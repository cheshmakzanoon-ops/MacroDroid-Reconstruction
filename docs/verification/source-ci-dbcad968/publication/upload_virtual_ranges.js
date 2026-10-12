async function uploadBatch(limit){
 const q=s=>"'"+s.replaceAll("'","'\\''")+"'";
 for(const row of load("dbcad_source_newblobs").filter(r=>!r.known&&!load("dbcad_source_uploaded")[r.git_blob_sha1]).slice(0,limit)){
  const CHUNK=737280,parts=[];for(let offset=0;offset<row.size_bytes;offset+=CHUNK)parts.push({offset,size:Math.min(CHUNK,row.size_bytes-offset)});
  let cache=load("dbcad_source_chunk_cache")||{};cache[row.git_blob_sha1]??={};store("dbcad_source_chunk_cache",cache);
  for(let attempt=0;attempt<3;attempt++){
   const missing=parts.filter(p=>!load("dbcad_source_chunk_cache")[row.git_blob_sha1][p.offset]);if(!missing.length)break;
   for(let start=0;start<missing.length;start+=3){
    const batch=missing.slice(start,start+3),rs=await Promise.allSettled(batch.map(async p=>{
     const py=row.encoding==='utf-8'?"import sys;f=open(sys.argv[1],'rb');f.seek(int(sys.argv[2]));sys.stdout.write(f.read(int(sys.argv[3])).decode('ascii'))":"import sys,base64;f=open(sys.argv[1],'rb');f.seek(int(sys.argv[2]));sys.stdout.write(base64.b64encode(f.read(int(sys.argv[3]))).decode())";
     let r=await tools.exec_command({cmd:"python3 -c "+q(py)+" "+q(row.source_path||("/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction/"+row.path))+" "+((row.source_offset||0)+p.offset)+" "+p.size,login:false,max_output_tokens:260000,yield_time_ms:1000});
     let out=r.output,n=0;while(r.session_id&&r.exit_code===undefined){if(++n>15)throw Error("bounded chunk timeout");r=await tools.write_stdin({session_id:r.session_id,chars:"",yield_time_ms:1000,max_output_tokens:260000});out+=r.output;}
     if(r.exit_code!==0||out.length!==(row.encoding==='utf-8'?p.size:4*Math.ceil(p.size/3)))throw Error("chunk transport length mismatch");
     return out;
    }));
    cache=load("dbcad_source_chunk_cache");const errors=[];
    for(let i=0;i<rs.length;i++){if(rs[i].status==="fulfilled")cache[row.git_blob_sha1][batch[i].offset]=rs[i].value;else errors.push(batch[i].offset);}
    store("dbcad_source_chunk_cache",cache);if(errors.length)notify({retry_offsets:errors,path:row.path,attempt:attempt+1});
   }
  }
  cache=load("dbcad_source_chunk_cache")[row.git_blob_sha1];if(parts.some(p=>!cache[p.offset]))throw Error("read incomplete after bounded retries");
  const content=parts.map(p=>cache[p.offset]).join("");if(content.length!==(row.encoding==='utf-8'?row.size_bytes:4*Math.ceil(row.size_bytes/3)))throw Error("whole transport size mismatch");
  const args={link_id:"link_6a9ea15de9248191931f1987300fc159",repository_full_name:"cheshmakzanoon-ops/MacroDroid-Reconstruction",encoding:row.encoding,content};if(JSON.stringify(args).length>16777216)throw Error("request cap exceeded");const result=await tools.mcp__codex_apps__github_create_blob(args);
  if(result.structuredContent?.sha!==row.git_blob_sha1)throw Error("remote blob digest mismatch");
  const uploaded=load("dbcad_source_uploaded");uploaded[row.git_blob_sha1]=true;store("dbcad_source_uploaded",uploaded);const allcache=load("dbcad_source_chunk_cache");delete allcache[row.git_blob_sha1];store("dbcad_source_chunk_cache",allcache);
  notify({uploaded:row.path,completed:Object.keys(uploaded).length,total:load("dbcad_source_newblobs").length});
 }
 text({uploaded_total:Object.keys(load("dbcad_source_uploaded")).length});
}

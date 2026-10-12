.class public abstract Lcom/arlosoft/macrodroid/triggers/Trigger;
.super Lcom/arlosoft/macrodroid/common/SelectableItem;
.source "r8-map-id-43b0b16dc0073b4b53e316177ca478d827b877826459072a6fdbad625fa2dd5f"

# interfaces
.implements Landroid/os/Parcelable;


# static fields
.field public static final enabledStateLock:Ljava/lang/Object;


# instance fields
.field private transient addingFavourite:Z

.field transient isTriggerEnabled:Z

.field private transient parentGUID:J

.field private transient parentSIGUIDForInsert:J


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 1
    new-instance v0, Ljava/lang/Object;

    .line 3
    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    .line 6
    sput-object v0, Lcom/arlosoft/macrodroid/triggers/Trigger;->enabledStateLock:Ljava/lang/Object;

    .line 8
    return-void
.end method

.method public constructor <init>()V
    .locals 1

    .line 1
    invoke-direct {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;-><init>()V

    .line 4
    return-void
.end method

.method public static U(Lk2e;Ljava/util/ArrayList;)V
    .locals 2

    .line 1
    const-string v1, "  ~@~@~@~@~@~@~@~@~@~@~   Smob - Mod obfuscation tool v1.4 by Kirlif\'   ~@~@~@~@~@~@~@~@~@~@~  "

    invoke-virtual {p0}, Lk2e;->allowedOnDevice()Z

    .line 4
    move-result v0

    .line 5
    if-eqz v0, :cond_b

    .line 7
    invoke-virtual {p1, p0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 10
    :cond_b
    return-void
.end method

.method public static e0(Landroid/content/Context;)Ljava/util/ArrayList;
    .locals 5

    .line 1
    const/4 v4, 0x1

    new-instance v0, Ljava/util/ArrayList;

    .line 3
    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 6
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/HeadphonesTriggerInfo;->getInstance()Lk2e;

    .line 9
    move-result-object v1

    .line 10
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 13
    const/4 v4, 0x6

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/BluetoothTriggerInfo;->getInstance()Lk2e;

    .line 16
    move-result-object v1

    .line 17
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 20
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/PowerButtonToggleTriggerInfo;->getInstance()Lk2e;

    .line 23
    move-result-object v1

    .line 24
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 27
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/BatteryLevelTriggerInfo;->getInstance()Lk2e;

    .line 30
    move-result-object v1

    .line 31
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 34
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AirplaneModeTriggerInfo;->getInstance()Lk2e;

    .line 37
    move-result-object v1

    .line 38
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 41
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/TimerTriggerInfo;->getInstance()Lk2e;

    .line 44
    move-result-object v1

    .line 45
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 48
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WidgetPressedTriggerInfo;->getInstance()Lk2e;

    .line 51
    move-result-object v1

    .line 52
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 55
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DialNumberTriggerInfo;->getInstance()Lk2e;

    .line 58
    move-result-object v1

    .line 59
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 62
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/IncomingSMSTriggerInfo;->getInstance()Lk2e;

    .line 65
    move-result-object v1

    .line 66
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 69
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/IncomingCallTriggerInfo;->getInstance()Lk2e;

    .line 72
    move-result-object v1

    .line 73
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 76
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ExternalPowerTriggerInfo;->getInstance()Lk2e;

    .line 79
    move-result-object v1

    .line 80
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 83
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WifiConnectionTriggerInfo;->getInstance()Lk2e;

    .line 86
    move-result-object v1

    .line 87
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 90
    const/4 v4, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/BootTriggerInfo;->getInstance()Lk2e;

    .line 93
    move-result-object v1

    .line 94
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 97
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SignalOnOffTriggerInfo;->getInstance()Lk2e;

    .line 100
    move-result-object v1

    .line 101
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 104
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/RegularIntervalTriggerInfo;->getInstance()Lk2e;

    .line 107
    move-result-object v1

    .line 108
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 111
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/LocationTriggerInfo;->getInstance()Lk2e;

    .line 114
    move-result-object v1

    .line 115
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 118
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ScreenOnOffTriggerInfo;->getInstance()Lk2e;

    .line 121
    move-result-object v1

    .line 122
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 125
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AppEnabledTriggerInfo;->getInstance()Lk2e;

    .line 128
    move-result-object v1

    .line 129
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 132
    const/4 v4, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ApplicationInstalledRemovedTriggerInfo;->getInstance()Lk2e;

    .line 135
    move-result-object v1

    .line 136
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 139
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ShakeDeviceTriggerInfo;->getInstance()Lk2e;

    .line 142
    move-result-object v1

    .line 143
    const/4 v4, 0x5

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 146
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DockTriggerInfo;->getInstance()Lk2e;

    .line 149
    move-result-object v1

    .line 150
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 153
    const/4 v4, 0x2

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SilentModeTriggerInfo;->getInstance()Lk2e;

    .line 156
    move-result-object v1

    .line 157
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 160
    const/4 v4, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/NotificationTriggerInfo;->getInstance()Lk2e;

    .line 163
    move-result-object v1

    .line 164
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 167
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WifiSSIDTriggerInfo;->getInstance()Lk2e;

    .line 170
    move-result-object v1

    .line 171
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 174
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ModeEnterExitTriggerInfo;->getInstance()Lk2e;

    .line 177
    move-result-object v1

    .line 178
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 181
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CallEndedTriggerInfo;->getInstance()Lk2e;

    .line 184
    move-result-object v1

    .line 185
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 188
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DataOnOffTriggerInfo;->getInstance()Lk2e;

    .line 191
    move-result-object v1

    .line 192
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 195
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DataUsedTriggerInfo;->getInstance()Lk2e;

    .line 198
    move-result-object v1

    .line 199
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 202
    const/4 v4, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FailedLoginTriggerInfo;->getInstance()Lk2e;

    .line 205
    move-result-object v1

    .line 206
    const/4 v4, 0x3

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 209
    const/4 v4, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ShortcutTriggerInfo;->getInstance()Lk2e;

    .line 212
    move-result-object v1

    .line 213
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 216
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FlipDeviceTriggerInfo;->getInstance()Lk2e;

    .line 219
    move-result-object v1

    .line 220
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 223
    const/4 v4, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ProximityTriggerInfo;->getInstance()Lk2e;

    .line 226
    move-result-object v1

    .line 227
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 230
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/VolumeButtonTriggerInfo;->getInstance()Lk2e;

    .line 233
    move-result-object v1

    .line 234
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 237
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/VolumeLongPressTriggerInfo;->getInstance()Lk2e;

    .line 240
    move-result-object v1

    .line 241
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 244
    const/4 v4, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/GPSEnabledTriggerInfo;->getInstance()Lk2e;

    .line 247
    move-result-object v1

    .line 248
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 251
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/OutgoingCallTriggerInfo;->getInstance()Lk2e;

    .line 254
    move-result-object v1

    .line 255
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 258
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SMSSentTriggerInfo;->getInstance()Lk2e;

    .line 261
    move-result-object v1

    .line 262
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 265
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/VariableTriggerInfo;->getInstance()Lk2e;

    .line 268
    move-result-object v1

    .line 269
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 272
    const/4 v4, 0x5

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DeviceUnlockedTriggerInfo;->getInstance()Lk2e;

    .line 275
    move-result-object v1

    .line 276
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 279
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/EmptyTriggerInfo;->getInstance()Lk2e;

    .line 282
    move-result-object v1

    .line 283
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 286
    const/4 v4, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/HotspotTriggerInfo;->getInstance()Lk2e;

    .line 289
    move-result-object v1

    .line 290
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 293
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MacroDroidInitialisedTriggerInfo;->getInstance()Lk2e;

    .line 296
    move-result-object v1

    .line 297
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 300
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MacroDroidEnabledTriggerInfo;->getInstance()Lk2e;

    .line 303
    move-result-object v1

    .line 304
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 307
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WeatherTriggerInfo;->getInstance()Lk2e;

    .line 310
    move-result-object v1

    .line 311
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 314
    const/4 v4, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CalendarTriggerInfo;->getInstance()Lk2e;

    .line 317
    move-result-object v1

    .line 318
    const/4 v4, 0x5

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 321
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AndroidWearTriggerInfo;->getInstance()Lk2e;

    .line 324
    move-result-object v1

    .line 325
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 328
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WearOSComplicationClickTriggerInfo;->getInstance()Lk2e;

    .line 331
    move-result-object v1

    .line 332
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 335
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CallActiveTriggerInfo;->getInstance()Lk2e;

    .line 338
    move-result-object v1

    .line 339
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 342
    const/4 v4, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DayTriggerInfo;->getInstance()Lk2e;

    .line 345
    move-result-object v1

    .line 346
    const/4 v4, 0x5

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 349
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CallMissedTriggerInfo;->getInstance()Lk2e;

    .line 352
    move-result-object v1

    .line 353
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 356
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ClipboardChangeTriggerInfo;->getInstance()Lk2e;

    .line 359
    move-result-object v1

    .line 360
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 363
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/NetworkRoamingChangedTriggerInfo;->getInstance()Lk2e;

    .line 366
    move-result-object v1

    .line 367
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 370
    const/4 v4, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SunriseSunsetTriggerInfo;->getInstance()Lk2e;

    .line 373
    move-result-object v1

    .line 374
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 377
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ActivityRecognitionTriggerInfo;->getInstance()Lk2e;

    .line 380
    move-result-object v1

    .line 381
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 384
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FloatingButtonTriggerInfo;->getInstance()Lk2e;

    .line 387
    move-result-object v1

    .line 388
    const/4 v4, 0x3

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 391
    const/4 v4, 0x0

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/StopwatchTriggerInfo;->getInstance()Lk2e;

    .line 394
    move-result-object v1

    .line 395
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 398
    const/4 v4, 0x6

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SystemTimeTriggerInfo;->getInstance()Lk2e;

    .line 401
    move-result-object v1

    .line 402
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 405
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AutoSyncChangeTriggerInfo;->getInstance()Lk2e;

    .line 408
    move-result-object v1

    .line 409
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 412
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CameraFlashlightTriggerInfo;->getInstance()Lk2e;

    .line 415
    move-result-object v1

    .line 416
    const/4 v4, 0x3

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 419
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CameraInUseTriggerInfo;->getInstance()Lk2e;

    .line 422
    move-result-object v1

    .line 423
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 426
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AutoRotateChangeTriggerInfo;->getInstance()Lk2e;

    .line 429
    move-result-object v1

    .line 430
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 433
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/BatterySaverTriggerInfo;->getInstance()Lk2e;

    .line 436
    move-result-object v1

    .line 437
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 440
    const/4 v4, 0x7

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/IntentReceivedTriggerInfo;->getInstance()Lcom/arlosoft/macrodroid/triggers/info/IntentReceivedTriggerInfo;

    .line 443
    move-result-object v1

    .line 444
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 447
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/OrientationTriggerInfo;->getInstance()Lcom/arlosoft/macrodroid/triggers/info/OrientationTriggerInfo;

    .line 450
    move-result-object v1

    .line 451
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 454
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SleepTriggerInfo;->getInstance()Lk2e;

    .line 457
    move-result-object v1

    .line 458
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 461
    invoke-virtual {p0}, Landroid/content/Context;->getPackageManager()Landroid/content/pm/PackageManager;

    .line 464
    move-result-object v1

    .line 465
    const/4 v4, 0x0

    const-string v2, ".esnlngde.dahgnowoairdiarrn.er_ashe"

    const-string v2, "android.hardware.sensor.hinge_angle"

    .line 467
    invoke-virtual {v1, v2}, Landroid/content/pm/PackageManager;->hasSystemFeature(Ljava/lang/String;)Z

    .line 470
    move-result v1

    .line 471
    const/4 v4, 0x1

    if-eqz v1, :cond_217

    .line 473
    const/4 v4, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FoldAngleTriggerInfo;->getInstance()Lk2e;

    .line 476
    move-result-object v1

    .line 477
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 480
    :cond_217
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MediaButtonPressedTriggerInfo;->getInstance()Lk2e;

    .line 483
    move-result-object v1

    .line 484
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 487
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MediaButtonV2TriggerInfo;->getInstance()Lk2e;

    .line 490
    move-result-object v1

    .line 491
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 494
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ApplicationLaunchedTriggerInfo;->getInstance()Lk2e;

    .line 497
    move-result-object v1

    .line 498
    const/4 v4, 0x5

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 501
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AppActivityLaunchedTriggerInfo;->getInstance()Lk2e;

    .line 504
    move-result-object v1

    .line 505
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 508
    const/4 v4, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SwipeTriggerInfo;->getInstance()Lk2e;

    .line 511
    move-result-object v1

    .line 512
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 515
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/NotificationButtonTriggerInfo;->getInstance()Lk2e;

    .line 518
    move-result-object v1

    .line 519
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 522
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DrawerOpenCloseTriggerInfo;->getInstance()Lk2e;

    .line 525
    move-result-object v1

    .line 526
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 529
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FloatingTextShownHiddenTriggerInfo;->getInstance()Lk2e;

    .line 532
    move-result-object v1

    .line 533
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 536
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/KeyboardOpenCloseTriggerInfo;->getInstance()Lk2e;

    .line 539
    move-result-object v1

    .line 540
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 543
    const/4 v4, 0x7

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MacroEnabledTriggerInfo;->getInstance()Lk2e;

    .line 546
    move-result-object v1

    .line 547
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 550
    const/4 v4, 0x2

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MacroFinishedTriggerInfo;->getInstance()Lk2e;

    .line 553
    move-result-object v1

    .line 554
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 557
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SystemLogTriggerInfo;->getInstance()Lk2e;

    .line 560
    move-result-object v1

    .line 561
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 564
    const/4 v4, 0x6

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DayDreamTriggerInfo;->getInstance()Lk2e;

    .line 567
    move-result-object v1

    .line 568
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 571
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/RecentAppsTriggerInfo;->getInstance()Lk2e;

    .line 574
    move-result-object v1

    .line 575
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 578
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MusicPlayingTriggerInfo;->getInstance()Lk2e;

    .line 581
    move-result-object v1

    .line 582
    const/4 v4, 0x3

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 585
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/QuickSettingsTileTriggerInfo;->getInstance()Lk2e;

    .line 588
    move-result-object v1

    .line 589
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 592
    const/4 v4, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/GeofenceTriggerInfo;->getInstance()Lk2e;

    .line 595
    move-result-object v1

    .line 596
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 599
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/NFCTriggerInfo;->getInstance()Lk2e;

    .line 602
    move-result-object v1

    .line 603
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 606
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/NFCStateTriggerInfo;->getInstance()Lk2e;

    .line 609
    move-result-object v1

    .line 610
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 613
    const/4 v4, 0x1

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/PebbleTriggerInfo;->getInstance()Lk2e;

    .line 616
    move-result-object v1

    .line 617
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 620
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CellTowerTriggerInfo;->getInstance()Lk2e;

    .line 623
    move-result-object v1

    .line 624
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 627
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/LightSensorTriggerInfo;->getInstance()Lk2e;

    .line 630
    move-result-object v1

    .line 631
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 634
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SensorTriggerInfo;->getInstance()Lk2e;

    .line 637
    move-result-object v1

    .line 638
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 641
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/LocalePluginTriggerInfo;->getInstance()Lk2e;

    .line 644
    move-result-object v1

    .line 645
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 648
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FingerprintGestureTriggerInfo;->getInstance()Lk2e;

    .line 651
    move-result-object v1

    .line 652
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 655
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/HomeButtonLongPressTriggerInfo;->getInstance()Lk2e;

    .line 658
    move-result-object v1

    .line 659
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 662
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/PowerButtonLongPressTriggerInfo;->getInstance()Lk2e;

    .line 665
    move-result-object v1

    .line 666
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 669
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/BluetoothBeaconTriggerInfo;->getInstance()Lk2e;

    .line 672
    move-result-object v1

    .line 673
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 676
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WebHookTriggerInfo;->getInstance()Lk2e;

    .line 679
    move-result-object v1

    .line 680
    const/4 v4, 0x1

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 683
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WebHook2wayTriggerInfo;->getInstance()Lk2e;

    .line 686
    move-result-object v1

    .line 687
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 690
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/HttpServerTriggerInfo;->getInstance()Lk2e;

    .line 693
    move-result-object v1

    .line 694
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 697
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/UsbDeviceConnectionTriggerInfo;->getInstance()Lk2e;

    .line 700
    move-result-object v1

    .line 701
    const/4 v4, 0x2

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 704
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/BatteryTemperatureTriggerInfo;->getInstance()Lk2e;

    .line 707
    move-result-object v1

    .line 708
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 711
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/PriorityModeTriggerInfo;->getInstance()Lcom/arlosoft/macrodroid/triggers/info/PriorityModeTriggerInfo;

    .line 714
    move-result-object v1

    .line 715
    const/4 v4, 0x5

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 718
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/LogcatTriggerInfo;->getInstance()Lk2e;

    .line 721
    move-result-object v1

    .line 722
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 725
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SimChangeTriggerInfo;->getInstance()Lk2e;

    .line 728
    move-result-object v1

    .line 729
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 732
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/DarkThemeTriggerInfo;->getInstance()Lk2e;

    .line 735
    move-result-object v1

    .line 736
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 739
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SystemSettingTriggerInfo;->getInstance()Lk2e;

    .line 742
    move-result-object v1

    .line 743
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 746
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/PhotoTakenTriggerInfo;->getInstance()Lcom/arlosoft/macrodroid/triggers/info/PhotoTakenTriggerInfo;

    .line 749
    move-result-object v1

    .line 750
    const/4 v4, 0x3

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 753
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/FileChangedTriggerInfo;->getInstance()Lk2e;

    .line 756
    move-result-object v1

    .line 757
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 760
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ScreenContentTriggerInfo;->getInstance()Lk2e;

    .line 763
    move-result-object v1

    .line 764
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 767
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ScreenshotContentTriggerInfo;->getInstance()Lk2e;

    .line 770
    move-result-object v1

    .line 771
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 774
    const/4 v4, 0x7

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/UIClickTriggerInfo;->getInstance()Lk2e;

    .line 777
    move-result-object v1

    .line 778
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 781
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/SpotifyTriggerInfo;->getInstance()Lk2e;

    .line 784
    move-result-object v1

    .line 785
    const/4 v4, 0x5

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 788
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MediaTrackChangedTriggerInfo;->getInstance()Lk2e;

    .line 791
    move-result-object v1

    .line 792
    const/4 v4, 0x3

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 795
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/MacroDroidIconLongPressShortcutTriggerInfo;->getInstance()Lk2e;

    .line 798
    move-result-object v1

    .line 799
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 802
    const/4 v4, 0x3

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AccessibilityServiceStateTriggerInfo;->getInstance()Lk2e;

    .line 805
    move-result-object v1

    .line 806
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 809
    const/4 v4, 0x2

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ToastTriggerInfo;->getInstance()Lk2e;

    .line 812
    move-result-object v1

    .line 813
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 816
    const/4 v4, 0x4

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ShareTextTriggerInfo;->getInstance()Lk2e;

    .line 819
    move-result-object v1

    .line 820
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 823
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ShareFileTriggerInfo;->getInstance()Lk2e;

    .line 826
    move-result-object v1

    .line 827
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 830
    const/4 v4, 0x2

    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/GoogleAssistantTriggerInfo;->getInstance()Lk2e;

    .line 833
    move-result-object v1

    .line 834
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 837
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/AssistantActivatedTriggerInfo;->getInstance()Lk2e;

    .line 840
    move-result-object v1

    .line 841
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 844
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/VpnTriggerInfo;->getInstance()Lcom/arlosoft/macrodroid/triggers/info/VpnTriggerInfo;

    .line 847
    move-result-object v1

    .line 848
    const/4 v4, 0x0

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 851
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/IpAddressChangeTriggerInfo;->getInstance()Lk2e;

    .line 854
    move-result-object v1

    .line 855
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 858
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/NetworkTransportChangeTriggerInfo;->getInstance()Lk2e;

    .line 861
    move-result-object v1

    .line 862
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 865
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/EmailReceivedTriggerInfo;->getInstance()Lk2e;

    .line 868
    move-result-object v1

    .line 869
    const/4 v4, 0x7

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 872
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/WorkProfileTriggerInfo;->getInstance()Lk2e;

    .line 875
    move-result-object v1

    .line 876
    const/4 v4, 0x4

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 879
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/ShizukuStoppedTriggerInfo;->getInstance()Lk2e;

    .line 882
    move-result-object v1

    .line 883
    const/4 v4, 0x6

    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 886
    invoke-static {}, Lcom/arlosoft/macrodroid/triggers/info/CustomSceneTriggerInfo;->getInstance()Lk2e;

    .line 889
    move-result-object v1

    .line 890
    invoke-static {v1, v0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->U(Lk2e;Ljava/util/ArrayList;)V

    .line 893
    invoke-static {p0}, Lcom/arlosoft/macrodroid/settings/c;->M(Landroid/content/Context;)Ljava/util/Locale;

    .line 896
    move-result-object v1

    .line 897
    invoke-static {v1}, Ljava/text/Collator;->getInstance(Ljava/util/Locale;)Ljava/text/Collator;

    .line 900
    move-result-object v1

    .line 901
    const/4 v4, 0x2

    const/4 v2, 0x0

    .line 902
    const/4 v4, 0x5

    invoke-virtual {v1, v2}, Ljava/text/Collator;->setStrength(I)V

    .line 905
    new-instance v2, Lo03;

    .line 907
    const/4 v4, 0x4

    const/4 v3, 0x1

    .line 908
    const/4 v4, 0x0

    invoke-direct {v2, v1, p0, v3}, Lo03;-><init>(Ljava/text/Collator;Landroid/content/Context;I)V

    .line 911
    invoke-static {v0, v2}, Ljava/util/Collections;->sort(Ljava/util/List;Ljava/util/Comparator;)V

    .line 914
    return-object v0
.end method


# virtual methods
.method public final T(Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;)V
    .locals 6

    .line 1
    const/4 v5, 0x4

    iget-wide v0, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentGUID:J

    .line 3
    const-wide/16 v2, 0x0

    const-wide/16 v2, 0x0

    .line 5
    cmp-long v4, v0, v2

    .line 7
    if-eqz v4, :cond_1c

    .line 9
    iget-object v2, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 11
    const/4 v5, 0x3

    invoke-virtual {v2, v0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->findChildByGUID(J)Lcom/arlosoft/macrodroid/common/SelectableItem;

    .line 14
    move-result-object v0

    .line 15
    instance-of v1, v0, Lcom/arlosoft/macrodroid/action/WaitUntilTriggerAction;

    .line 17
    if-eqz v1, :cond_5a

    .line 19
    check-cast v0, Lcom/arlosoft/macrodroid/action/WaitUntilTriggerAction;

    .line 21
    invoke-virtual {v0, p0}, Lcom/arlosoft/macrodroid/action/WaitUntilTriggerAction;->k0(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 24
    goto :goto_5a

    .line 25
    :cond_1c
    iget-wide v0, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentSIGUIDForInsert:J

    .line 27
    cmp-long v0, v0, v2

    .line 29
    const/4 v5, 0x0

    if-nez v0, :cond_2a

    .line 31
    iget-object v0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 33
    const/4 v5, 0x7

    invoke-virtual {v0, p0}, Lcom/arlosoft/macrodroid/macro/Macro;->addTrigger(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 36
    goto :goto_5a

    .line 37
    :cond_2a
    const/4 v5, 0x1

    const/4 v0, 0x0

    .line 38
    :goto_2c
    const/4 v5, 0x1

    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 40
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerList()Ljava/util/ArrayList;

    .line 43
    move-result-object v1

    .line 44
    invoke-virtual {v1}, Ljava/util/ArrayList;->size()I

    .line 47
    move-result v1

    .line 48
    if-ge v0, v1, :cond_5a

    .line 50
    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 52
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerList()Ljava/util/ArrayList;

    .line 55
    move-result-object v1

    .line 56
    invoke-virtual {v1, v0}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;

    .line 59
    move-result-object v1

    .line 60
    check-cast v1, Lcom/arlosoft/macrodroid/triggers/Trigger;

    .line 62
    const/4 v5, 0x5

    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSIGUID()J

    .line 65
    move-result-wide v1

    .line 66
    iget-wide v3, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentSIGUIDForInsert:J

    .line 68
    const/4 v5, 0x1

    cmp-long v1, v1, v3

    .line 70
    if-nez v1, :cond_57

    .line 72
    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 74
    invoke-virtual {v1, p0, v0}, Lcom/arlosoft/macrodroid/macro/Macro;->addTriggerAtIndex(Lcom/arlosoft/macrodroid/triggers/Trigger;I)V

    .line 77
    goto :goto_5a

    .line 78
    :cond_57
    add-int/lit8 v0, v0, 0x1

    .line 80
    goto :goto_2c

    .line 81
    :cond_5a
    :goto_5a
    check-cast p1, Lm88;

    .line 83
    const/4 p0, 0x0

    .line 84
    const/4 v5, 0x4

    invoke-interface {p1, p0}, Lm88;->t(Lzpf;)V

    .line 87
    const/4 v5, 0x7

    return-void
.end method

.method public final W(Z)V
    .locals 3

    .line 1
    const/4 v0, 0x1

    .line 2
    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->checkAllPermissions(Z)Z

    .line 5
    move-result v0

    .line 6
    const/4 v2, 0x4

    if-nez v0, :cond_30

    .line 8
    const/4 v2, 0x0

    new-instance v0, Ljava/lang/StringBuilder;

    .line 10
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    .line 13
    const/4 v2, 0x5

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroName()Ljava/lang/String;

    .line 16
    move-result-object v1

    .line 17
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 20
    const-string v1, " - "

    .line 22
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 25
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 28
    move-result-object v1

    .line 29
    const/4 v2, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 32
    const-string v1, "  missing permission"

    .line 34
    const/4 v2, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 37
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 40
    move-result-object v0

    .line 41
    invoke-static {v0}, Lkjf;->h(Ljava/lang/String;)V

    .line 44
    :cond_30
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->isEnabled()Z

    .line 47
    move-result v0

    .line 48
    const/4 v2, 0x1

    if-eqz v0, :cond_3b

    .line 50
    const/4 v2, 0x2

    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/triggers/Trigger;->c0(Z)V

    .line 53
    :cond_3b
    return-void
.end method

.method public abstract X()V
.end method

.method public final Z()V
    .locals 3

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/triggers/Trigger;->enabledStateLock:Ljava/lang/Object;

    .line 3
    monitor-enter v0

    .line 4
    :try_start_3
    const/4 v2, 0x4

    iget-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z

    .line 6
    if-nez v1, :cond_e

    .line 8
    const/4 v2, 0x2

    monitor-exit v0

    .line 9
    const/4 v2, 0x2

    return-void

    .line 10
    :catchall_c
    move-exception p0

    .line 11
    goto :goto_17

    .line 12
    :cond_e
    const/4 v1, 0x0

    .line 13
    iput-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z

    .line 15
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->X()V

    .line 18
    const/4 v2, 0x5

    monitor-exit v0

    .line 19
    return-void

    .line 20
    :goto_17
    monitor-exit v0
    :try_end_18
    .catchall {:try_start_3 .. :try_end_18} :catchall_c

    .line 21
    const/4 v2, 0x2

    throw p0
.end method

.method public abstract a0()V
.end method

.method public b0(Z)V
    .locals 1

    .line 1
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->a0()V

    .line 4
    const/4 v0, 0x2

    return-void
.end method

.method public final c0(Z)V
    .locals 4

    .line 1
    sget-object v0, Lcom/arlosoft/macrodroid/triggers/Trigger;->enabledStateLock:Ljava/lang/Object;

    .line 3
    const/4 v3, 0x4

    monitor-enter v0

    .line 4
    :try_start_4
    iget-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z

    .line 6
    if-eqz v1, :cond_d

    .line 8
    monitor-exit v0

    .line 9
    return-void

    .line 10
    :catchall_a
    move-exception p0

    .line 11
    const/4 v3, 0x3

    goto :goto_4a

    .line 12
    :cond_d
    const/4 v1, 0x1

    .line 13
    const/4 v3, 0x0

    iput-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z
    :try_end_11
    .catchall {:try_start_4 .. :try_end_11} :catchall_a

    .line 15
    :try_start_11
    const/4 v3, 0x4

    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/triggers/Trigger;->b0(Z)V
    :try_end_15
    .catch Ljava/lang/Exception; {:try_start_11 .. :try_end_15} :catch_16
    .catchall {:try_start_11 .. :try_end_15} :catchall_a

    .line 18
    goto :goto_48

    .line 19
    :catch_16
    move-exception p1

    .line 20
    const/4 v3, 0x5

    const/4 v1, 0x0

    .line 21
    :try_start_19
    iput-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z

    .line 23
    new-instance v1, Ljava/lang/StringBuilder;

    .line 25
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 28
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroName()Ljava/lang/String;

    .line 31
    move-result-object v2

    .line 32
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 35
    const-string v2, " - "

    .line 37
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 40
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getConfiguredName()Ljava/lang/String;

    .line 43
    move-result-object p0

    .line 44
    const/4 v3, 0x0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 47
    const-string p0, " - failed to enable trigger: "

    .line 49
    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 52
    const/4 v3, 0x5

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    .line 55
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 58
    move-result-object p0

    .line 59
    const/4 v3, 0x4

    invoke-static {p0}, Lkjf;->h(Ljava/lang/String;)V

    .line 62
    invoke-static {p1}, Lsz5;->e(Ljava/lang/Throwable;)V

    .line 65
    :goto_48
    monitor-exit v0

    .line 66
    return-void

    .line 67
    :goto_4a
    monitor-exit v0
    :try_end_4b
    .catchall {:try_start_19 .. :try_end_4b} :catchall_a

    .line 68
    const/4 v3, 0x7

    throw p0
.end method

.method public f0()Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;
    .locals 2

    .line 1
    new-instance v0, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 3
    const/4 v1, 0x4

    invoke-direct {v0, p0}, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;-><init>(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 6
    const/4 v1, 0x7

    return-object v0
.end method

.method public final g0()Z
    .locals 1

    .line 1
    iget-boolean p0, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->isTriggerEnabled:Z

    .line 3
    return p0
.end method

.method public final getAlertDialogTheme()I
    .locals 1

    .line 1
    const p0, 0x7f150360

    .line 4
    return p0
.end method

.method public final getDialogTheme()I
    .locals 1

    .line 1
    const/4 v0, 0x0

    const p0, 0x7f150360

    .line 4
    return p0
.end method

.method public final getLogEntryStart()Ljava/lang/String;
    .locals 1

    .line 1
    const/4 v0, 0x6

    const-string p0, "T: "

    .line 3
    const/4 v0, 0x7

    return-object p0
.end method

.method public h0()V
    .locals 1

    .line 1
    return-void
.end method

.method public final i0(J)V
    .locals 1

    .line 1
    iput-wide p1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentGUID:J

    .line 3
    const/4 v0, 0x5

    return-void
.end method

.method public itemComplete()V
    .locals 9

    .line 1
    invoke-super {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->itemComplete()V

    .line 4
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getActivity()Landroid/app/Activity;

    .line 7
    move-result-object v0

    .line 8
    const/4 v8, 0x5

    instance-of v1, v0, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;

    .line 10
    const/4 v2, -0x1

    .line 11
    if-eqz v1, :cond_6b

    .line 13
    iget-boolean v1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->addingFavourite:Z

    .line 15
    const/4 v8, 0x1

    const/4 v3, 0x0

    .line 16
    if-eqz v1, :cond_26

    .line 18
    move-object v1, v0

    .line 19
    const/4 v8, 0x2

    check-cast v1, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 21
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/triggers/Trigger;->T(Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;)V

    .line 24
    const/4 v8, 0x3

    iput-boolean v3, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->addingFavourite:Z

    .line 26
    check-cast v0, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;

    .line 28
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;->P1()V

    .line 31
    invoke-virtual {v0, v3}, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;->D1(Z)V

    .line 34
    return-void

    .line 35
    :cond_26
    const/4 v8, 0x2

    iget-wide v4, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentGUID:J

    .line 37
    const-wide/16 v6, 0x0

    .line 39
    cmp-long v1, v4, v6

    .line 41
    if-eqz v1, :cond_41

    .line 43
    const/4 v8, 0x7

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 45
    invoke-virtual {p0, v4, v5}, Lcom/arlosoft/macrodroid/macro/Macro;->findChildByGUID(J)Lcom/arlosoft/macrodroid/common/SelectableItem;

    .line 48
    move-result-object p0

    .line 49
    instance-of v0, p0, Lcom/arlosoft/macrodroid/action/WaitUntilTriggerAction;

    .line 51
    if-eqz v0, :cond_9a

    .line 53
    check-cast p0, Lcom/arlosoft/macrodroid/action/WaitUntilTriggerAction;

    .line 55
    const/4 v8, 0x1

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/action/WaitUntilTriggerAction;->l0()V

    .line 58
    return-void

    .line 59
    :cond_41
    instance-of v1, p0, Lcom/arlosoft/macrodroid/triggers/AndroidWearTrigger;

    .line 61
    if-eqz v1, :cond_59

    .line 63
    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 65
    invoke-virtual {v1}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerList()Ljava/util/ArrayList;

    .line 68
    move-result-object v1

    .line 69
    const/4 v8, 0x3

    invoke-virtual {v1, p0}, Ljava/util/ArrayList;->contains(Ljava/lang/Object;)Z

    .line 72
    move-result v1

    .line 73
    const/4 v8, 0x0

    if-nez v1, :cond_59

    .line 75
    iget-object v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 77
    const/4 v8, 0x4

    invoke-virtual {v1, p0}, Lcom/arlosoft/macrodroid/macro/Macro;->addTrigger(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 80
    :cond_59
    new-instance p0, Landroid/content/Intent;

    .line 82
    invoke-direct {p0}, Landroid/content/Intent;-><init>()V

    .line 85
    invoke-virtual {v0, v2, p0}, Landroid/app/Activity;->setResult(ILandroid/content/Intent;)V

    .line 88
    check-cast v0, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;

    .line 90
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;->P1()V

    .line 93
    invoke-virtual {v0, v3}, Lcom/arlosoft/macrodroid/editscreen/EditMacroActivity;->D1(Z)V

    .line 96
    const/4 v8, 0x2

    return-void

    .line 97
    :cond_6b
    iget-boolean v1, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_returnOnComplete:Z

    .line 99
    if-eqz v1, :cond_87

    .line 101
    const/4 v8, 0x6

    new-instance v1, Landroid/content/Intent;

    .line 103
    const/4 v8, 0x4

    invoke-direct {v1}, Landroid/content/Intent;-><init>()V

    .line 106
    const-string v2, "Macro"

    .line 108
    const/4 v8, 0x7

    iget-object p0, p0, Lcom/arlosoft/macrodroid/common/SelectableItem;->m_macro:Lcom/arlosoft/macrodroid/macro/Macro;

    .line 110
    invoke-virtual {v1, v2, p0}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Landroid/os/Parcelable;)Landroid/content/Intent;

    .line 113
    const/4 p0, 0x1

    .line 114
    const/4 v8, 0x5

    invoke-virtual {v0, p0, v1}, Landroid/app/Activity;->setResult(ILandroid/content/Intent;)V

    .line 117
    invoke-virtual {v0}, Landroid/app/Activity;->finish()V

    .line 120
    return-void

    .line 121
    :cond_87
    instance-of v1, v0, Lcom/arlosoft/macrodroid/selectableitemlist/AddTriggerActivity;

    .line 123
    const/4 v8, 0x7

    if-eqz v1, :cond_9a

    .line 125
    move-object v1, v0

    .line 126
    check-cast v1, Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;

    .line 128
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/triggers/Trigger;->T(Lcom/arlosoft/macrodroid/app/base/MacroDroidBaseActivity;)V

    .line 131
    const/4 v8, 0x7

    invoke-virtual {v0, v2}, Landroid/app/Activity;->setResult(I)V

    .line 134
    const/4 v8, 0x2

    invoke-virtual {v0}, Landroid/app/Activity;->finish()V

    .line 137
    :cond_9a
    return-void
.end method

.method public final j0(J)V
    .locals 1

    .line 1
    iput-wide p1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentSIGUIDForInsert:J

    .line 3
    const/4 v0, 0x6

    return-void
.end method

.method public k0()Z
    .locals 1

    .line 1
    instance-of p0, p0, Lcom/arlosoft/macrodroid/triggers/InvokedByAnimationOverlayTrigger;

    .line 3
    xor-int/lit8 p0, p0, 0x1

    .line 5
    return p0
.end method

.method public final l0()V
    .locals 4

    .line 1
    new-instance v0, Ljava/lang/StringBuilder;

    .line 3
    const-string/jumbo v1, "t nmgg riesTir:te"

    const-string v1, "Testing trigger: "

    .line 5
    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 8
    const/4 v3, 0x7

    new-instance v1, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 10
    const/4 v3, 0x4

    invoke-direct {v1, p0}, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;-><init>(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 13
    const/4 v3, 0x4

    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 16
    move-result-object v1

    .line 17
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 20
    const/4 v3, 0x4

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 23
    move-result-object v0

    .line 24
    const/4 v3, 0x6

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 27
    move-result-object v1

    .line 28
    invoke-virtual {v1}, Ljava/lang/Long;->longValue()J

    .line 31
    move-result-wide v1

    .line 32
    invoke-static {v1, v2, v0}, Lkjf;->m(JLjava/lang/String;)V

    .line 35
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 38
    move-result-object v0

    .line 39
    invoke-virtual {v0, p0}, Lcom/arlosoft/macrodroid/macro/Macro;->setTriggerThatInvoked(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 42
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->f0()Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 45
    move-result-object p0

    .line 46
    const/4 v3, 0x5

    if-eqz p0, :cond_3b

    .line 48
    invoke-virtual {v0, p0}, Lcom/arlosoft/macrodroid/macro/Macro;->setTriggerContextInfo(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)V

    .line 51
    :cond_3b
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerContextInfo()Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 54
    move-result-object p0

    .line 55
    const/4 v1, 0x2

    const/4 v1, 0x1

    .line 56
    const/4 v3, 0x2

    invoke-virtual {v0, p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->invokeActions(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Z)V

    .line 59
    const/4 v3, 0x0

    return-void
.end method

.method public final m0()V
    .locals 4

    .line 1
    const/4 v3, 0x7

    new-instance v0, Ljava/lang/StringBuilder;

    .line 3
    const/4 v3, 0x4

    const-string v1, "Testing trigger with constraints: "

    .line 5
    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    .line 8
    new-instance v1, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 10
    invoke-direct {v1, p0}, Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;-><init>(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 13
    invoke-virtual {p0, v1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getSystemLogEntryName(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Ljava/lang/String;

    .line 16
    move-result-object v1

    .line 17
    const/4 v3, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 20
    const/4 v3, 0x0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    .line 23
    move-result-object v0

    .line 24
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacroGuid()Ljava/lang/Long;

    .line 27
    move-result-object v1

    .line 28
    invoke-virtual {v1}, Ljava/lang/Long;->longValue()J

    .line 31
    move-result-wide v1

    .line 32
    invoke-static {v1, v2, v0}, Lkjf;->m(JLjava/lang/String;)V

    .line 35
    const/4 v3, 0x2

    const/4 v0, 0x0

    .line 36
    const/4 v3, 0x5

    invoke-virtual {p0, v0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->constraintsMet(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)Z

    .line 39
    move-result v0

    .line 40
    const/4 v3, 0x6

    const/4 v1, 0x1

    .line 41
    if-eqz v0, :cond_4a

    .line 43
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getMacro()Lcom/arlosoft/macrodroid/macro/Macro;

    .line 46
    move-result-object v0

    .line 47
    invoke-virtual {v0, p0}, Lcom/arlosoft/macrodroid/macro/Macro;->setTriggerThatInvoked(Lcom/arlosoft/macrodroid/triggers/Trigger;)V

    .line 50
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->f0()Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 53
    move-result-object p0

    .line 54
    const/4 v3, 0x1

    if-eqz p0, :cond_42

    .line 56
    invoke-virtual {v0, p0}, Lcom/arlosoft/macrodroid/macro/Macro;->setTriggerContextInfo(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;)V

    .line 59
    :cond_42
    invoke-virtual {v0}, Lcom/arlosoft/macrodroid/macro/Macro;->getTriggerContextInfo()Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;

    .line 62
    move-result-object p0

    .line 63
    invoke-virtual {v0, p0, v1}, Lcom/arlosoft/macrodroid/macro/Macro;->invokeActions(Lcom/arlosoft/macrodroid/triggers/TriggerContextInfo;Z)V

    .line 66
    return-void

    .line 67
    :cond_4a
    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/common/SelectableItem;->getContext()Landroid/content/Context;

    .line 70
    move-result-object p0

    .line 71
    const/4 v3, 0x4

    const v0, 0x7f14074c

    .line 74
    invoke-static {p0, v0, v1}, Le3g;->a(Landroid/content/Context;II)Le3g;

    .line 77
    move-result-object p0

    .line 78
    const/4 v3, 0x5

    invoke-virtual {p0}, Le3g;->show()V

    .line 81
    return-void
.end method

.method public final onItemSelected(JJZ)V
    .locals 1

    .line 1
    iput-wide p1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentGUID:J

    .line 3
    iput-wide p3, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->parentSIGUIDForInsert:J

    .line 5
    const/4 p1, 0x1

    .line 6
    const/4 v0, 0x1

    invoke-virtual {p0, p1}, Lcom/arlosoft/macrodroid/common/SelectableItem;->onItemSelected(Z)V

    .line 9
    return-void
.end method

.method public secondaryItemConfirmed()V
    .locals 1

    .line 1
    const/4 v0, 0x4

    invoke-virtual {p0}, Lcom/arlosoft/macrodroid/triggers/Trigger;->itemComplete()V

    .line 4
    return-void
.end method

.method public final setAddingFavourite(Z)V
    .locals 1

    .line 1
    iput-boolean p1, p0, Lcom/arlosoft/macrodroid/triggers/Trigger;->addingFavourite:Z

    .line 3
    return-void
.end method

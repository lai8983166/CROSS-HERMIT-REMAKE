
void FUN__text1__008494b6(undefined4 *param_1)

{
  DWORD DVar1;
  undefined4 uVar2;
  _TIME_ZONE_INFORMATION local_d0;
  _SYSTEMTIME local_24;
  _SYSTEMTIME local_14;
  
  GetLocalTime(&local_14);
  GetSystemTime(&local_24);
  if (local_24.wMinute == DAT_008756b0._2_2_) {
    if (local_24.wHour == (WORD)DAT_008756b0) {
      if (local_24.wDay == DAT_008756ac._2_2_) {
        if (local_24.wMonth == DAT_008756a8._2_2_) {
          if (local_24.wYear == (WORD)DAT_008756a8) goto LAB__text1__00849560;
        }
      }
    }
  }
  DVar1 = GetTimeZoneInformation(&local_d0);
  if (DVar1 == 0xffffffff) {
    DAT_008756a0 = 0xffffffff;
  }
  else if (((DVar1 == 2) && (local_d0.DaylightDate.wMonth != 0)) && (local_d0.DaylightBias != 0)) {
    DAT_008756a0 = 1;
  }
  else {
    DAT_008756a0 = 0;
  }
  DAT_008756a8._0_2_ = local_24.wYear;
  DAT_008756a8._2_2_ = local_24.wMonth;
  DAT_008756ac._0_2_ = local_24.wDayOfWeek;
  DAT_008756ac._2_2_ = local_24.wDay;
  DAT_008756b0._0_2_ = local_24.wHour;
  DAT_008756b0._2_2_ = local_24.wMinute;
  DAT_008756b4._0_2_ = local_24.wSecond;
  DAT_008756b4._2_2_ = local_24.wMilliseconds;
LAB__text1__00849560:
  uVar2 = FUN__text1__0084a2c4
                    (local_14.wYear,local_14.wMonth,local_14.wDay,local_14.wHour,local_14.wMinute,
                     local_14.wSecond,DAT_008756a0);
  if (param_1 != (undefined4 *)0x0) {
    *param_1 = uVar2;
  }
  return;
}


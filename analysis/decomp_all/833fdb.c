
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int FUN__text1__00833fdb(void)

{
  int iVar1;
  code *pcVar2;
  int iVar3;
  HMODULE local_60;
  HWND local_54;
  int local_50;
  uint local_4c;
  undefined4 local_48;
  code *local_44;
  undefined4 *local_40;
  undefined *local_3c;
  undefined4 *local_38;
  int local_34;
  int local_30;
  undefined4 local_2c;
  uint *local_28;
  undefined *local_24;
  HMODULE local_20;
  undefined4 local_1c;
  int local_18;
  code *local_14;
  undefined4 local_10;
  uint local_c;
  int local_8;
  
  FUN__text1__00811040((DAT_0086e3c8 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 3);
  local_50 = FUN__text1__0083428d();
  if (local_50 == 0) {
    DAT_008750d8 = 1;
    local_8 = 0;
  }
  else {
    iVar3 = local_50 + 8;
    local_4c = local_4c & 0xffffff00;
    if (((DAT_00874e98 == 1) && ((*DAT_00874ea0 == '/' || (*DAT_00874ea0 == '-')))) &&
       ((iVar1 = FUN__text1__0084e5b0(DAT_00874ea0 + 1,&DAT_0086e5bc,1), iVar1 == 0 ||
        (iVar1 = FUN__text1__0084e5b0(DAT_00874ea0 + 1,&DAT_0086e5b8,1), iVar1 == 0)))) {
      local_4c = CONCAT31(local_4c._1_3_,1);
    }
    local_54 = (HWND)0x0;
    iVar3 = FUN__text1__00834345(iVar3,&local_54,local_4c & 0xff);
    if (iVar3 == 0) {
      local_8 = 0;
    }
    else {
      iVar3 = FUN__text1__008346e0(iVar3);
      if (iVar3 == 0) {
        local_8 = 0;
      }
      else {
        iVar1 = (*DAT_008750d0)(DAT_008750cc,1,0);
        if (iVar1 == 0) {
          DAT_008750d8 = 5;
          local_8 = 0;
        }
        else {
          pcVar2 = (code *)FUN__text1__00834f90(DAT_008750cc,"SetFunctionAddresses");
          (*pcVar2)(PTR_IMAGE_DOS_HEADER_008751e8,FUN__text1__008107d0,FUN__text1__00810eb8,
                    FUN__text1__00810ed2,FUN__text1__00810f2b,FUN__text1__0081132e,
                    FUN__text1__00811f90,FUN__text1__00836597,FUN__text1__00833fc9,
                    FUN__text1__00836208,
                    DAT_0086e398 ^ _DAT_0086e3f8 ^ _DAT_0086e3d8 ^ _DAT_0086e3fc,&local_44,&local_48
                    ,&local_10);
          local_14 = local_44;
          DAT_00874ec0 = local_48;
          DAT_00874ebc = local_10;
          local_c = (uint)((local_4c & 0xff) != 0);
          if (DAT_008751f0 != '\0') {
            local_c = local_c | 2;
            FreeConsole();
          }
          if ((DAT_008751f0 != '\0') && (local_54 != (HWND)0x0)) {
            DestroyWindow(local_54);
            local_54 = (HWND)0x0;
          }
          local_40 = &DAT_008750d8;
          local_3c = &DAT_008750dc;
          local_38 = &DAT_0086e380;
          local_30 = local_50;
          local_2c = DAT_008751ec;
          local_28 = &local_c;
          local_24 = &DAT_00874ec4;
          local_34 = iVar3;
          if (DAT_00874e98 == 2) {
            local_60 = DAT_00874eb4;
          }
          else {
            local_60 = GetModuleHandleA((LPCSTR)0x0);
          }
          local_20 = local_60;
          local_1c = DAT_0086e37c;
          local_18 = -1;
          local_8 = (*local_14)(&local_40);
          if (local_18 == -1) {
            if (local_8 != 1) {
              DAT_008753dc = 1;
            }
          }
          else {
            DAT_008753dc = local_18;
          }
          if (local_54 != (HWND)0x0) {
            DestroyWindow(local_54);
          }
        }
      }
    }
  }
  return local_8;
}


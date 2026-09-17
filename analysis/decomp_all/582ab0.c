
/* Library Function - Single Match
    _crtGetLocaleInfoA@16
   
   Library: Visual Studio 2003 Debug
   __stdcall crtGetLocaleInfoA,16 */

undefined4 crtGetLocaleInfoA(uint param_1,uint param_2,char *param_3,int param_4)

{
  int iVar1;
  undefined4 uVar2;
  int local_14;
  undefined **local_c;
  int local_8;
  
  local_14 = 0;
  local_8 = 0x1a;
  local_c = (undefined **)0x0;
  do {
    if (local_8 < local_14) {
LAB__text__00582c18:
      uVar2 = (*API_KERNEL32_DLL_GetLocaleInfoA)(param_1,param_2,param_3,param_4);
      return uVar2;
    }
    iVar1 = (local_14 + local_8) / 2;
    if (param_1 == *(uint *)(&DAT_00764720 + iVar1 * 0x2c)) {
      if (param_2 < 0xc) {
        if (param_2 == 0xb) {
          local_c = (undefined **)(&DAT_0076473c + iVar1 * 0x2c);
        }
        else if (param_2 == 1) {
          local_c = (undefined **)(&DAT_00764724 + iVar1 * 0x2c);
        }
        else if (param_2 == 3) {
          local_c = &PTR_DAT_00764730 + iVar1 * 0xb;
        }
        else if (param_2 == 7) {
          local_c = &PTR_DAT_00764738 + iVar1 * 0xb;
        }
      }
      else if (param_2 == 0x1001) {
        local_c = (undefined **)(&PTR_s_Spanish___Traditional_Sort_0076472c)[iVar1 * 0xb];
      }
      else if (param_2 == 0x1002) {
        local_c = (undefined **)(&PTR_s_Spain_00764734)[iVar1 * 0xb];
      }
      else if (param_2 == 0x1004) {
        local_c = (undefined **)(&DAT_00764744 + iVar1 * 0x2c);
      }
      if ((local_c != (undefined **)0x0) && (0 < param_4)) {
        _strncpy(param_3,(char *)local_c,param_4 - 1);
        param_3[param_4 + -1] = '\0';
        return 1;
      }
      goto LAB__text__00582c18;
    }
    if (param_1 < *(uint *)(&DAT_00764720 + iVar1 * 0x2c)) {
      local_8 = iVar1 + -1;
    }
    else {
      local_14 = iVar1 + 1;
    }
  } while( true );
}


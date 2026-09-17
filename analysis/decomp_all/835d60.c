
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4
FUN__text1__00835d60(undefined *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  char *_Str;
  int iVar1;
  size_t sVar2;
  undefined4 uVar3;
  char *_Str_00;
  char *local_14;
  undefined4 local_c;
  
  PTR_IMAGE_DOS_HEADER_008751e8 = param_1;
  DAT_00874e98 = 1;
  _DAT_00874e9c = param_4;
  DAT_00874ea0 = param_3;
  PTR_IMAGE_DOS_HEADER_00874ea4 = param_1;
  FUN__text1__0083e283(param_1,2);
  _Str = operator_new(0x2000);
  _memset(_Str,0,0x2000);
  local_c = FUN__text1__00836119(param_3,_Str);
  iVar1 = FUN__text1__0084e5b0(_Str,"SERVER",6);
  if (iVar1 == 0) {
    DAT_008751f0 = 1;
    DAT_0086e37c = 0x3c;
    sVar2 = _strlen(_Str);
    if (6 < sVar2) {
      iVar1 = __strcmpi(_Str + 6,"X");
      if (iVar1 == 0) {
        DAT_0086e37c = 0xffffffff;
      }
      else {
        iVar1 = __strcmpi(_Str + 6,"DOWN");
        if (iVar1 == 0) {
          DAT_0086e37c = 0xfffffffe;
        }
        else {
          local_14 = _Str + 6;
          while ((*local_14 != '\0' && (iVar1 = FUN__text1__0084948e((int)*local_14), iVar1 != 0)))
          {
            local_14 = local_14 + 1;
          }
          if (*local_14 == '\0') {
            DAT_0086e37c = FUN__text1__00849483(_Str + 6);
          }
          else {
            DAT_008751f0 = 0;
          }
        }
      }
    }
    local_c = FUN__text1__00836119(local_c,_Str);
  }
  iVar1 = __strcmpi(_Str,"REGISTER");
  if (iVar1 == 0) {
    DAT_008751ec = 1;
    FUN__text1__00848d20(&DAT_00874ec4,local_c);
  }
  else {
    iVar1 = __strcmpi(_Str,"QUIETREGISTER");
    if (iVar1 == 0) {
      DAT_008751ec = 8;
      FUN__text1__00848d20(&DAT_00874ec4,local_c);
    }
    else {
      iVar1 = __strcmpi(_Str,"TRANSFER");
      if (iVar1 == 0) {
        DAT_008751ec = 2;
      }
      else {
        iVar1 = __strcmpi(_Str,"FIXCLOCK");
        if (iVar1 == 0) {
          DAT_008751ec = 3;
        }
        else {
          iVar1 = __strcmpi(_Str,"INFO");
          if (iVar1 == 0) {
            DAT_008751ec = 4;
          }
          else {
            iVar1 = __strcmpi(_Str,"UNREGISTER");
            if (iVar1 == 0) {
              DAT_008751ec = 5;
            }
            else {
              iVar1 = __strcmpi(_Str,"QUIETUNREGISTER");
              if (iVar1 == 0) {
                DAT_008751ec = 9;
              }
              else {
                iVar1 = __strcmpi(_Str,"SHOWNETUSERS");
                if (iVar1 == 0) {
                  DAT_008751ec = 6;
                }
                else {
                  iVar1 = __strcmpi(_Str,"HWCHANGELOG");
                  if (iVar1 == 0) {
                    DAT_008751ec = 7;
                  }
                  else {
                    iVar1 = __strcmpi(_Str,"QUIETEXIT");
                    if (iVar1 == 0) {
                      DAT_008751ec = 10;
                    }
                    else {
                      iVar1 = FUN__text1__0084e5b0(_Str,"ARMDEBUG=",9);
                      if (iVar1 == 0) {
                        FUN__text1__00848d20(&DAT_00874ec4,_Str + 9);
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  iVar1 = FUN__text1__00835864();
  if (iVar1 == 0) {
    uVar3 = FUN__text1__00833f91();
    FUN__text1__00848d20(_Str,uVar3);
    _Str_00 = (char *)FUN__text1__00833fa2();
    sVar2 = _strlen(_Str_00);
    if (sVar2 != 0) {
      FUN__text1__00848d30(_Str,&DAT_0086e6dc);
      uVar3 = FUN__text1__00833fa2();
      FUN__text1__00848d30(_Str,uVar3);
    }
    MessageBoxA((HWND)0x0,_Str,(LPCSTR)0x0,0x40010);
  }
  uVar3 = DAT_008753dc;
  FUN__text1__00848476(_Str);
  return uVar3;
}


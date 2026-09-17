
void FUN__text__0041f340(undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4,
                        undefined4 param_5,undefined4 param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  char *local_14;
  size_t local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = (char *)FUN__text__004214f0(param_2,param_3);
  iVar2 = FUN__text__004209f0(local_14);
  if (iVar2 == 0) {
    local_c = FUN__text__004048d0(param_1,0,local_14,1,1,param_5,param_6);
  }
  else {
    iVar2 = FUN__text__00420b50(local_14);
    if (iVar2 == 0) {
      local_c = FUN__text__00404fb0(param_1,0,local_14,1,1,param_5);
    }
    else {
      local_18 = FUN__text__004214f0(param_2,param_3 + 1);
      if (local_18 - (int)local_14 == 0x10) {
        (*API_KERNEL32_DLL_lstrlenA)("Dm-No-MakeTex");
        local_10 = FUN__text__0056ce80();
        iVar2 = _strncmp(local_14,"Dm-No-MakeTex",local_10);
        if (iVar2 == 0) goto LAB__text__0041f46c;
      }
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexTbl.cpp",
                                  DAT_005ff5d4 + 0x14,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
LAB__text__0041f46c:
  local_8 = 0x41f479;
  FUN__text__0056ce80();
  return;
}



int FUN__text__0052a8fd(undefined4 *param_1,undefined4 param_2,undefined4 *param_3,
                       undefined4 *param_4,undefined4 *param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 uStack_42c;
  undefined4 uStack_428;
  undefined4 *puStack_424;
  undefined4 uStack_420;
  undefined4 uStack_41c;
  undefined4 *puStack_418;
  undefined4 *puStack_414;
  undefined4 *puStack_410;
  
  puStack_410 = (undefined4 *)0x52a911;
  FUN__text__0053b6ae();
  puStack_410 = (undefined4 *)0x52a91c;
  FUN__text__0053ea5a();
  if (param_3 != (undefined4 *)0x0) {
    *param_3 = 0;
  }
  if (param_4 != (undefined4 *)0x0) {
    *param_4 = 0;
  }
  if (param_5 != (undefined4 *)0x0) {
    *param_5 = 0;
  }
  puStack_410 = (undefined4 *)0x1;
  puStack_414 = param_1;
  puStack_418 = (undefined4 *)0x52a946;
  iVar2 = FUN__text__0053b6c0();
  pcVar1 = API_KERNEL32_DLL_WideCharToMultiByte;
  if (-1 < iVar2) {
    puStack_410 = (undefined4 *)0x0;
    puStack_414 = (undefined4 *)0x0;
    puStack_418 = (undefined4 *)0x0;
    uStack_41c = 0;
    uStack_420 = 0xffffffff;
    puStack_424 = param_1;
    uStack_428 = 0;
    uStack_42c = 0;
    uVar3 = (*API_KERNEL32_DLL_WideCharToMultiByte)();
    FUN__text__0056e230();
    (*pcVar1)(0,0,param_1,0xffffffff,&uStack_42c,uVar3,0,0);
    puStack_410 = param_5;
    puStack_414 = param_4;
    puStack_418 = param_3;
    uStack_41c = param_2;
    uStack_420 = 1;
    puStack_424 = &uStack_42c;
    iVar2 = FUN__text__00540ec8();
    iVar4 = 0;
    if (-1 < iVar2) goto LAB__text__0052a9a4;
  }
  iVar4 = iVar2;
LAB__text__0052a9a4:
  puStack_410 = (undefined4 *)0x52a9af;
  FUN__text__0053eb03();
  puStack_410 = (undefined4 *)0x52a9b7;
  FUN__text__0053b8db();
  return iVar4;
}


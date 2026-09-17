
void FUN__text__004271e0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_2c54 [16];
  uint local_2c14;
  undefined1 *local_2c10;
  undefined1 local_2c0c [10240];
  undefined1 local_40c [964];
  undefined4 uStack_48;
  undefined1 *puStack_44;
  char *pcStack_40;
  int iStack_3c;
  undefined1 *puStack_38;
  int iStack_34;
  undefined4 uStack_30;
  undefined1 *puStack_2c;
  undefined4 uStack_28;
  int iStack_24;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  undefined4 uStack_14;
  
  FUN__text__0056e230();
  puVar2 = local_2c54;
  for (iVar1 = 0xb14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  uStack_14 = param_1;
  uStack_18 = 0x42720b;
  iVar1 = FUN__text__0056cd38();
  if (iVar1 != 0) {
    local_2c10 = local_2c0c;
    uStack_18 = 0;
    uStack_1c = 0;
    uStack_20 = 0;
    uStack_28 = 0x427234;
    iStack_24 = iVar1;
    uStack_28 = FUN__text__0056cd68();
    puStack_2c = local_2c10;
    uStack_30 = 0;
    puStack_38 = (undefined1 *)0x42724d;
    iStack_34 = iVar1;
    FUN__text__0056cd68();
    for (local_2c14 = 0; local_2c14 < *(uint *)(local_2c10 + 8); local_2c14 = local_2c14 + 1) {
      puStack_38 = local_2c10 + *(int *)(local_2c10 + local_2c14 * 4 + 0x18);
      iStack_3c = local_2c14 + 1;
      pcStack_40 = "%2d. %s\r\n";
      puStack_44 = local_40c;
      uStack_48 = 0x4272ae;
      (*API_USER32_DLL_wsprintfA)();
      puStack_38 = (undefined1 *)0x4272b8;
      FUN__text__0056ce80();
    }
    iStack_3c = param_1;
    pcStack_40 = (char *)0x4272c7;
    puStack_38 = (undefined1 *)iVar1;
    FUN__text__0056cd2c();
  }
  FUN__text__0056ce80();
  return;
}


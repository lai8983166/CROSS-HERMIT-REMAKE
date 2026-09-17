
void FUN__text__0048c170(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                        undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined *local_1c;
  undefined1 local_18 [4];
  undefined2 local_14;
  undefined4 local_10;
  undefined4 local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_1c = &DAT_006c2dc8 + param_1 * 0x48;
  FUN__text__0048b6c0(param_1,&local_1c);
  _memset(local_18,0,0x10);
  local_14 = (undefined2)param_1;
  local_10 = FUN__text__0048b720(param_1,0xe,param_2);
  FUN__text__0048c850(param_1,0xe,0,local_18,param_2,param_3,param_4,param_5);
  local_8 = 0x48c209;
  FUN__text__0056ce80();
  return;
}


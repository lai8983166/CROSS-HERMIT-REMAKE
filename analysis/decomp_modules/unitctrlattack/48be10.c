
void FUN__text__0048be10(int param_1,int param_2,undefined4 param_3,undefined4 param_4,
                        undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined *local_1c;
  undefined1 local_18 [4];
  undefined2 local_14;
  undefined4 local_10;
  short local_a;
  undefined4 local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_1c = &DAT_006c2dc8 + param_1 * 0x48;
  _memset(local_18,0,0x10);
  local_14 = (undefined2)param_1;
  local_10 = FUN__text__0048b720(param_1,10,param_2);
  iVar1 = FUN__text__0046c9f0(param_1);
  if (iVar1 == 0) {
    local_a = *(short *)(local_1c + 0x28) +
              (short)((int)((uint)*(byte *)(*(int *)(param_2 + 600) + 7) *
                           (int)*(short *)(local_1c + 0x2a)) / 100);
  }
  else {
    local_a = *(short *)(*(int *)(param_2 + 600) + 0x42);
  }
  FUN__text__0048c850(param_1,10,0,local_18,param_2,param_3,param_4,param_5);
  local_8 = 0x48beeb;
  FUN__text__0056ce80();
  return;
}


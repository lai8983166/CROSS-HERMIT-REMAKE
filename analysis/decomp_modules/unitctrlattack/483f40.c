
void FUN__text__00483f40(undefined4 param_1,undefined4 param_2,undefined4 *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_b4 [16];
  int local_74;
  int local_70;
  undefined1 local_6c [44];
  undefined1 local_40 [40];
  short local_18;
  undefined4 local_14;
  undefined2 local_10;
  undefined1 uStack_e;
  undefined1 uStack_d;
  undefined2 local_c;
  short sStack_a;
  undefined4 local_8;
  
  puVar2 = local_b4;
  for (iVar1 = 0x2c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004deaa0(param_1,local_40);
  FUN__text__004deaa0(param_2,local_6c);
  FUN__text__0046b3e0(param_1,local_40);
  FUN__text__0046b3e0(param_2,local_6c);
  local_70 = FUN__text__004824d0(local_40,local_6c);
  if ((local_70 != 0) && (iVar1 = FUN__text__004692e0(param_2), iVar1 != 0)) {
    local_70 = 1;
  }
  local_14 = *param_3;
  uStack_d = (undefined1)((uint)param_3[1] >> 0x18);
  _local_10 = CONCAT12((undefined1)local_70,(short)param_3[1]);
  _local_c = CONCAT22(-local_18,(short)param_3[2]);
  FUN__text__00482d60((int)*(short *)(param_3 + 1),local_70,param_1,param_2,&local_14);
  local_74 = local_70;
  if (0 < local_70) {
    if (local_70 < 4) {
      FUN__text__0046beb0(param_2,0xbcc,0,0,0,&local_14);
    }
    else if (local_70 == 4) {
      FUN__text__0046beb0(param_2,0xbcc,0,0,0,&local_14);
    }
  }
  local_8 = 0x48407a;
  FUN__text__0056ce80();
  return;
}


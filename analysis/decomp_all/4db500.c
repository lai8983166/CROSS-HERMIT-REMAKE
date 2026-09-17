
void FUN__text__004db500(int param_1,void *param_2)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  int local_30;
  uint local_2c;
  int local_28;
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  uint local_14;
  int local_10;
  int local_c;
  undefined *local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &DAT_006c2ea0;
  _memset(param_2,0,0x24);
  local_10 = (int)*(short *)(local_8 + 0x20);
  local_14 = (uint)*(byte *)(param_1 + 0xc);
  local_18 = (int)*(short *)(local_8 + 0x22);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 10) = uVar1;
  local_1c = (int)*(short *)(local_8 + 0x24);
  local_20 = (uint)*(byte *)(param_1 + 0xc);
  local_24 = (int)*(short *)(local_8 + 0x26);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 8) = uVar1;
  local_28 = (int)*(short *)(local_8 + 0x28);
  local_2c = (uint)*(byte *)(param_1 + 0xc);
  local_30 = (int)*(short *)(local_8 + 0x2a);
  local_c = __ftol();
  local_c = -local_c;
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0xe) = uVar1;
  local_8 = (undefined *)0x4db63e;
  FUN__text__0056ce80();
  return;
}



void FUN__text__004dbb80(int param_1,void *param_2)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  uint local_14;
  int local_10;
  undefined4 local_c;
  undefined *local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &DAT_006c3170;
  _memset(param_2,0,0x24);
  local_10 = (int)*(short *)(local_8 + 0x20);
  local_14 = (uint)*(byte *)(param_1 + 0x3c);
  local_18 = (int)*(short *)(local_8 + 0x22);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0x12) = uVar1;
  local_1c = (int)*(short *)(local_8 + 0x24);
  local_20 = (uint)*(byte *)(param_1 + 0x34);
  local_24 = (int)*(short *)(local_8 + 0x26);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0x14) = uVar1;
  local_8 = (undefined *)0x4dbc66;
  FUN__text__0056ce80();
  return;
}


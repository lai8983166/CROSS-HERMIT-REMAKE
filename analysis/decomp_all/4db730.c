
void FUN__text__004db730(int param_1,void *param_2)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_88 [16];
  int local_48;
  uint local_44;
  int local_40;
  int local_3c;
  uint local_38;
  int local_34;
  int local_30;
  uint local_2c;
  int local_28;
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  uint local_14;
  int local_10;
  undefined4 local_c;
  undefined *local_8;
  
  puVar3 = local_88;
  for (iVar2 = 0x21; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &DAT_006c3008;
  _memset(param_2,0,0x24);
  local_10 = (int)*(short *)(local_8 + 0x20);
  local_14 = (uint)*(byte *)(param_1 + 0x14);
  local_18 = (int)*(short *)(local_8 + 0x22);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 10) = uVar1;
  local_1c = (int)*(short *)(local_8 + 0x24);
  local_20 = (uint)*(byte *)(param_1 + 0x14);
  local_24 = (int)*(short *)(local_8 + 0x26);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 8) = uVar1;
  local_28 = (int)*(short *)(local_8 + 0x28);
  local_2c = (uint)*(byte *)(param_1 + 0x14);
  local_30 = (int)*(short *)(local_8 + 0x2a);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 6) = uVar1;
  local_34 = (int)*(short *)(local_8 + 0x2c);
  local_38 = (uint)*(byte *)(param_1 + 0x14);
  local_3c = (int)*(short *)(local_8 + 0x2e);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0xc) = uVar1;
  local_40 = (int)*(short *)(local_8 + 0x30);
  local_44 = (uint)*(byte *)(param_1 + 0x14);
  local_48 = (int)*(short *)(local_8 + 0x32);
  local_c = __ftol();
  uVar1 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0xe) = uVar1;
  local_8 = (undefined *)0x4db91e;
  FUN__text__0056ce80();
  return;
}


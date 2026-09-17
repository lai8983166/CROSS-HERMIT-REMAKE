
void FUN__text__004dbc70(int param_1,void *param_2)

{
  byte bVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  uint local_14;
  int local_10;
  undefined4 local_c;
  undefined *local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = &DAT_006c3290;
  _memset(param_2,0,0x24);
  local_10 = (int)*(short *)(local_8 + 0x20);
  local_14 = (uint)*(byte *)(param_1 + 0x1c);
  local_18 = (int)*(short *)(local_8 + 0x26);
  local_c = __ftol();
  bVar1 = FUN__text__004dbd70(local_c,999);
  *(ushort *)((int)param_2 + 0x12) = (ushort)bVar1;
  uVar2 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0x12) = uVar2;
  local_c = 0;
  bVar1 = FUN__text__004dbd70(0,999);
  *(ushort *)((int)param_2 + 0x14) = (ushort)bVar1;
  uVar2 = FUN__text__004db650(local_c,0xffff8300,32000);
  *(undefined2 *)((int)param_2 + 0x14) = uVar2;
  local_8 = (undefined *)0x4dbd5f;
  FUN__text__0056ce80();
  return;
}


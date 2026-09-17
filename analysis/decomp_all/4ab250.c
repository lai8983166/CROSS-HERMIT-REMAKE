
int FUN__text__004ab250(ushort param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  short local_c;
  
  sVar1 = DAT_007d57de;
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  while( true ) {
    if (DAT_007d57de <= local_c) {
      *(ushort *)(&DAT_007d57e2 + DAT_007d57de * 2) = param_1;
      DAT_007d57de = DAT_007d57de + 1;
      return CONCAT31((int3)(char)((ushort)sVar1 >> 8),1);
    }
    if ((int)*(short *)(&DAT_007d57e2 + local_c * 2) == (uint)param_1) break;
    local_c = local_c + 1;
  }
  return (uint)(uint3)(int3)(char)((ushort)local_c >> 8) << 8;
}


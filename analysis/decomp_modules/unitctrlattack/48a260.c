
uint FUN__text__0048a260(int param_1,int param_2,int param_3,int param_4)

{
  byte bVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [17];
  uint local_c;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  bVar1 = *(byte *)(param_1 + 1);
  if (bVar1 < 3) {
    if (bVar1 == 2) {
      local_c = (uint)*(ushort *)(param_4 + 4) + (uint)*(byte *)(param_2 + 0x14) +
                ((uint)*(byte *)(*(int *)(param_3 + 600) + 4) * (uint)*(byte *)(param_2 + 0x15)) /
                100;
    }
    else if (bVar1 == 0) {
      local_c = (uint)*(ushort *)(param_4 + 4);
    }
    else if (bVar1 == 1) {
      local_c = (uint)*(ushort *)(param_4 + 4);
    }
  }
  else if (bVar1 == 3) {
    local_c = (uint)*(ushort *)(param_4 + 4) + (uint)*(byte *)(param_2 + 0x14) +
              ((uint)*(byte *)(*(int *)(param_3 + 600) + 6) * (uint)*(byte *)(param_2 + 0x15)) / 100
    ;
  }
  else if (bVar1 == 0xff) {
    local_c = 0xff;
  }
  *(undefined2 *)(param_4 + 4) = (undefined2)local_c;
  return local_c;
}


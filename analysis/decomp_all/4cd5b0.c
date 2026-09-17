
ushort FUN__text__004cd5b0(int param_1,undefined4 *param_2)

{
  bool bVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [17];
  undefined1 *local_1c;
  uint local_10;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = 0;
  local_10 = 0;
  bVar1 = false;
  local_1c = (undefined1 *)*param_2;
  *local_1c = 0;
  do {
    if (*(char *)(param_1 + local_10) == '\0') {
      *local_1c = 0;
      local_1c = local_1c + 1;
      uVar2 = uVar2 + 1;
      bVar1 = true;
    }
    else if (*(char *)(param_1 + local_10) == '\\') {
      *local_1c = 0;
      uVar2 = uVar2 + 1;
      local_1c = (undefined1 *)param_2[uVar2];
      local_10 = (uint)(ushort)((short)local_10 + 2);
    }
    else {
      *local_1c = *(undefined1 *)(param_1 + local_10);
      local_1c[1] = *(undefined1 *)(param_1 + (uint)(ushort)((short)local_10 + 1));
      local_1c = local_1c + 2;
      local_10 = (uint)(ushort)((short)local_10 + 2);
    }
  } while (!bVar1);
  return uVar2;
}


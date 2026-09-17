
int FUN_005798f0(int param_1)

{
  int iVar1;
  char cVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  undefined4 local_2c;
  undefined4 local_24;
  undefined4 local_c;
  undefined4 local_8;
  
  iVar3 = *(int *)(param_1 + 0x10);
  local_c = *(int *)(param_1 + 8);
  local_2c = 0;
  for (; -1 < local_c; local_c = local_c << 1) {
    local_2c = local_2c + 1;
  }
  iVar1 = iVar3 + 0x144 + local_2c * 0x204;
  for (local_24 = 0; local_24 < 0x3f; local_24 = local_24 + 1) {
    iVar4 = iVar1 + local_24 * 8;
    *(int *)(iVar4 + 8) = iVar4;
    *(int *)(iVar4 + 4) = iVar4;
  }
  uVar5 = *(int *)(param_1 + 0xc) + local_2c * 0x8000;
  iVar4 = (*API_KERNEL32_DLL_VirtualAlloc)(uVar5,0x8000,0x1000,4);
  if (iVar4 == 0) {
    local_2c = -1;
  }
  else {
    for (local_8 = uVar5; local_8 <= uVar5 + 0x7000; local_8 = local_8 + 0x1000) {
      *(undefined4 *)(local_8 + 8) = 0xffffffff;
      *(undefined4 *)(local_8 + 0xffc) = 0xffffffff;
      *(undefined4 *)(local_8 + 0xc) = 0xff0;
      *(uint *)(local_8 + 0x10) = local_8 + 0x100c;
      *(uint *)(local_8 + 0x14) = local_8 - 0xff4;
      *(undefined4 *)(local_8 + 0xff8) = 0xff0;
    }
    *(uint *)(iVar1 + 0x1fc) = uVar5 + 0xc;
    *(int *)(*(int *)(iVar1 + 0x1fc) + 8) = iVar1 + 0x1f8;
    *(uint *)(iVar1 + 0x200) = uVar5 + 0x700c;
    *(int *)(*(int *)(iVar1 + 0x200) + 4) = iVar1 + 0x1f8;
    *(undefined4 *)(iVar3 + 0x44 + local_2c * 4) = 0;
    *(undefined4 *)(iVar3 + 0xc4 + local_2c * 4) = 1;
    cVar2 = *(char *)(iVar3 + 0x43);
    *(char *)(iVar3 + 0x43) = *(char *)(iVar3 + 0x43) + '\x01';
    if (cVar2 == '\0') {
      *(uint *)(param_1 + 4) = *(uint *)(param_1 + 4) | 1;
    }
    *(uint *)(param_1 + 8) = *(uint *)(param_1 + 8) & ~(0x80000000U >> ((byte)local_2c & 0x1f));
  }
  return local_2c;
}


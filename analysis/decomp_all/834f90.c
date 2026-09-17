
int FUN__text1__00834f90(int param_1,char *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint local_10;
  
  iVar4 = param_1 + *(int *)(param_1 + *(int *)(param_1 + 0x3c) + 0x78);
  iVar1 = *(int *)(iVar4 + 0x20);
  iVar2 = *(int *)(iVar4 + 0x24);
  iVar3 = *(int *)(iVar4 + 0x1c);
  local_10 = 0;
  while( true ) {
    if (*(uint *)(iVar4 + 0x18) <= local_10) {
      return 0;
    }
    iVar5 = __strcmpi((char *)(param_1 + *(int *)(param_1 + iVar1 + local_10 * 4)),param_2);
    if (iVar5 == 0) break;
    local_10 = local_10 + 1;
  }
  return param_1 + *(int *)(param_1 + iVar3 + (uint)*(ushort *)(param_1 + iVar2 + local_10 * 2) * 4)
  ;
}


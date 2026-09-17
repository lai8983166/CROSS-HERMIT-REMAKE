
void FUN__text__0048eda0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((*(ushort *)(param_1 + 2) != (ushort)*(byte *)(param_2 + 1)) &&
     (iVar2 = FUN__text__00424f80("wk->workno == comw->from",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                  DAT_00618fb4 + 4,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = (uint)*(ushort *)(param_2 + 6);
  local_c._0_1_ = (char)*(ushort *)(param_2 + 6);
  switch(local_10) {
  case 0:
    *(char *)(*(int *)(param_1 + 600) + 0x9f) = (char)local_c;
    break;
  case 1:
    *(char *)(*(int *)(param_1 + 600) + 0x9f) = (char)local_c;
    *(char *)(param_1 + 0x2e8) =
         (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                     (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)(param_1 + 0x2e9) =
         (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                     (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    break;
  case 2:
    *(char *)(*(int *)(param_1 + 600) + 0x9f) = (char)local_c;
    break;
  case 3:
    *(char *)(*(int *)(param_1 + 600) + 0x9f) = (char)local_c;
    break;
  case 4:
    *(char *)(*(int *)(param_1 + 600) + 0xa0) = (char)local_c + -4;
    break;
  case 5:
    *(char *)(*(int *)(param_1 + 600) + 0xa0) = (char)local_c + -4;
    break;
  case 6:
    *(char *)(*(int *)(param_1 + 600) + 0xa0) = (char)local_c + -4;
    break;
  case 7:
    *(char *)(*(int *)(param_1 + 600) + 0xa0) = (char)local_c + -4;
  }
  local_8 = 0x48ef33;
  local_c = local_10;
  FUN__text__0056ce80();
  return;
}


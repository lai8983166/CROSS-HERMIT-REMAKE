
void __thiscall FUN__text__004398d0(int param_1,int param_2,int param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  char *local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(char **)(param_4 + 8);
  local_8 = param_1;
  if ((*local_c == '@') &&
     (*(int *)(*(int *)(param_1 + 0x88) + (param_3 * *(int *)(param_1 + 0x30) + param_2) * 4) != 0))
  {
    iVar2 = FUN__text__00424f80("NodePos[y*cellw+x]==0",
                                "E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",DAT_005ff9c4 + 2
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((*local_c == -0x80) &&
     (*(int *)(*(int *)(local_8 + 0x88) + (param_3 * *(int *)(local_8 + 0x30) + param_2) * 4) == 0))
  {
    iVar2 = FUN__text__00424f80("NodePos[y*cellw+x]!=0",
                                "E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",DAT_005ff9c4 + 3
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(int *)(*(int *)(local_8 + 0x88) + (param_3 * *(int *)(local_8 + 0x30) + param_2) * 4) = param_4;
  local_8 = 0x4399ba;
  FUN__text__0056ce80();
  return;
}



void __fastcall FUN__text__005483fc(int param_1)

{
  int *piVar1;
  code *pcVar2;
  int *piVar3;
  int iVar4;
  
  if (*(int *)(param_1 + 100) != 0) {
    (**(code **)(**(int **)(param_1 + 4) + 0xe0))(*(int **)(param_1 + 4),*(int *)(param_1 + 100));
  }
  if (*(int *)(param_1 + 0x68) != 0) {
    (**(code **)(**(int **)(param_1 + 4) + 0xe0))(*(int **)(param_1 + 4),*(int *)(param_1 + 0x68));
  }
  piVar3 = (int *)(param_1 + 0x10);
  iVar4 = 8;
  do {
    piVar1 = (int *)piVar3[8];
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      piVar3[8] = 0;
    }
    piVar1 = (int *)*piVar3;
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      *piVar3 = 0;
    }
    piVar3 = piVar3 + 1;
    iVar4 = iVar4 + -1;
  } while (iVar4 != 0);
  piVar3 = *(int **)(param_1 + 0xc);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0xc) = 0;
  }
  piVar3 = *(int **)(param_1 + 4);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 4) = 0;
  }
  pcVar2 = API_GDI32_DLL_SelectObject;
  if ((*(int *)(param_1 + 0x6c) != 0) && (*(int *)(param_1 + 0xa8) != 0)) {
    (*API_GDI32_DLL_SelectObject)(*(int *)(param_1 + 0x6c),*(int *)(param_1 + 0xa8));
  }
  if ((*(int *)(param_1 + 0x6c) != 0) && (*(int *)(param_1 + 0x9c) != 0)) {
    (*pcVar2)(*(int *)(param_1 + 0x6c),*(int *)(param_1 + 0x9c));
  }
  if (*(int *)(param_1 + 0x98) != 0) {
    (*API_GDI32_DLL_DeleteObject)(*(int *)(param_1 + 0x98));
  }
  if (*(int *)(param_1 + 0x6c) != 0) {
    (*API_GDI32_DLL_DeleteDC)(*(int *)(param_1 + 0x6c));
  }
  piVar3 = &DAT_0080a398;
  if (DAT_0080a398 != 0) {
    do {
      if (*piVar3 == param_1) break;
      piVar3 = (int *)(*piVar3 + 0xac);
    } while (*piVar3 != 0);
    if (*piVar3 != 0) {
      *piVar3 = *(int *)(*piVar3 + 0xac);
    }
  }
  return;
}


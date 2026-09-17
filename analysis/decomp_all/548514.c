
undefined4 __fastcall FUN__text__00548514(int param_1)

{
  int *piVar1;
  int *piVar2;
  uint uVar3;
  
  if (*(int *)(param_1 + 0x60) == 0) {
    piVar1 = (int *)(param_1 + 100);
    if ((*piVar1 == 0) || (*(int *)(param_1 + 0x68) == 0)) {
      uVar3 = 0;
      do {
        (**(code **)(**(int **)(param_1 + 4) + 0xd0))(*(int **)(param_1 + 4));
        (**(code **)(**(int **)(param_1 + 4) + 200))(*(int **)(param_1 + 4),7,0);
        piVar2 = piVar1;
        if (uVar3 != 0) {
          piVar2 = (int *)(param_1 + 0x68);
        }
        (**(code **)(**(int **)(param_1 + 4) + 0xd4))(*(int **)(param_1 + 4),piVar2);
        uVar3 = uVar3 + 1;
      } while (uVar3 < 2);
    }
    (**(code **)(**(int **)(param_1 + 0xc) + 0x10))(*(int **)(param_1 + 0xc));
    (**(code **)(**(int **)(param_1 + 4) + 0xdc))(*(int **)(param_1 + 4),*piVar1);
    (**(code **)(**(int **)(param_1 + 4) + 0xd8))
              (*(int **)(param_1 + 4),*(undefined4 *)(param_1 + 0x68));
    *(undefined4 *)(param_1 + 0x60) = 1;
    return 0;
  }
  return 0x8876086c;
}


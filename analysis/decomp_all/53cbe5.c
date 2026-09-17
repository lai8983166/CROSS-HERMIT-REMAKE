
undefined4 __fastcall FUN__text__0053cbe5(int param_1)

{
  int *piVar1;
  
  piVar1 = (int *)(param_1 + 0x470);
  if (*piVar1 == 0) {
    (**(code **)(**(int **)(param_1 + 8) + 0xd0))(*(int **)(param_1 + 8));
    (**(code **)(**(int **)(param_1 + 8) + 0xa0))(*(int **)(param_1 + 8),param_1 + 0x474);
    (**(code **)(**(int **)(param_1 + 8) + 200))
              (*(int **)(param_1 + 8),7,*(undefined4 *)(param_1 + 0x14));
    (**(code **)(**(int **)(param_1 + 8) + 0xd4))(*(int **)(param_1 + 8),piVar1);
  }
  (**(code **)(**(int **)(param_1 + 8) + 0xdc))(*(int **)(param_1 + 8),*piVar1);
  (**(code **)(**(int **)(param_1 + 8) + 0x80))(*(int **)(param_1 + 8),param_1 + 0x28);
  (**(code **)(**(int **)(param_1 + 8) + 0x84))(*(int **)(param_1 + 8),param_1 + 0x2c);
  return 0;
}



void __thiscall FUN__text__0040d390(int param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int *local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
        (*(int *)(param_1 + 0x10) != 0)) && ((-2 < param_4 && (param_4 < 0x40)))) &&
      ((-1 < param_2 && ((param_2 < 0x14 && (-1 < param_3)))))) &&
     ((param_3 < 0x78 &&
      (local_10 = (int *)(param_1 + 0x14 + param_2 * 0x5a0 + param_3 * 0xc), *local_10 != 0)))) {
    local_8 = param_1;
    if (param_4 != -1) {
      FUN__text__0040d4d0(param_4);
      *(undefined2 *)(local_8 + 0x7094 + param_4 * 4) = (undefined2)param_2;
      *(undefined2 *)(local_8 + 0x7096 + param_4 * 4) = (undefined2)param_3;
    }
    (**(code **)(**(int **)(local_8 + 8) + 0xb4))
              (*(undefined4 *)(local_8 + 8),
               *(undefined4 *)(local_8 + 0x14 + param_2 * 0x5a0 + param_3 * 0xc),0,0,0x80,0,0,0,0,0)
    ;
    local_c = FUN__text__0056ce80();
  }
  local_8 = 0x40d4c3;
  FUN__text__0056ce80();
  return;
}



void __thiscall FUN__text__0040d4d0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
      (*(int *)(param_1 + 0x10) != 0)) && ((-1 < param_2 && (param_2 < 0x40)))) {
    local_c = *(short *)(param_1 + 0x7094 + param_2 * 4);
    local_10 = *(short *)(param_1 + 0x7096 + param_2 * 4);
    if ((((-1 < local_c) && ((local_c < 0x14 && (-1 < local_10)))) && (local_10 < 0x78)) &&
       (*(int *)(param_1 + 0x14 + local_c * 0x5a0 + local_10 * 0xc) != 0)) {
      local_8 = param_1;
      (**(code **)(**(int **)(param_1 + 8) + 0xb8))
                (*(undefined4 *)(param_1 + 8),
                 *(undefined4 *)(param_1 + 0x14 + local_c * 0x5a0 + local_10 * 0xc),0,0,0);
      FUN__text__0056ce80();
      *(undefined2 *)(local_8 + 0x7094 + param_2 * 4) = 0xffff;
      *(undefined2 *)(local_8 + 0x7096 + param_2 * 4) = 0xffff;
    }
  }
  local_8 = 0x40d600;
  FUN__text__0056ce80();
  return;
}


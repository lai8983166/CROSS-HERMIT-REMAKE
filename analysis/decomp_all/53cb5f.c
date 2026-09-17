
undefined4 __thiscall
FUN__text__0053cb5f(int param_1,int *param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  if (param_2 == (int *)0x0) {
    uVar2 = 0x8876086c;
  }
  else {
    *(int **)(param_1 + 8) = param_2;
    (**(code **)(*param_2 + 4))(param_2);
    puVar1 = (undefined4 *)(param_1 + 0xc);
    *puVar1 = param_3;
    *(undefined4 *)(param_1 + 0x1c) = param_4;
    *(undefined4 *)(param_1 + 0x10) = param_5;
    *(undefined4 *)(param_1 + 0x14) = param_6;
    *(undefined4 *)(param_1 + 0x18) = param_7;
    FUN__text__0052755e(*(undefined4 *)(param_1 + 8),puVar1,puVar1,(undefined4 *)(param_1 + 0x1c),0,
                        (undefined4 *)(param_1 + 0x10),0);
    *(undefined4 *)(param_1 + 0x484) = 0;
    *(undefined4 *)(param_1 + 0x474) = 0;
    *(undefined4 *)(param_1 + 0x478) = 0;
    *(undefined4 *)(param_1 + 0x488) = 0x3f800000;
    *(undefined4 *)(param_1 + 0x47c) = *puVar1;
    *(undefined4 *)(param_1 + 0x480) = *puVar1;
    uVar2 = 0;
  }
  return uVar2;
}


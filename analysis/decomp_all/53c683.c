
undefined4 __thiscall
FUN__text__0053c683(int param_1,int *param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  undefined4 uVar1;
  
  if (param_2 == (int *)0x0) {
    uVar1 = 0x8876086c;
  }
  else if (*(int *)(param_1 + 8) == 0) {
    *(int **)(param_1 + 8) = param_2;
    (**(code **)(*param_2 + 4))(param_2);
    *(undefined4 *)(param_1 + 0xc) = param_3;
    *(undefined4 *)(param_1 + 0x10) = param_4;
    *(undefined4 *)(param_1 + 0x14) = param_5;
    *(undefined4 *)(param_1 + 0x18) = param_6;
    *(undefined4 *)(param_1 + 0x1c) = param_7;
    uVar1 = 0;
  }
  else {
    uVar1 = 0x80004005;
  }
  return uVar1;
}


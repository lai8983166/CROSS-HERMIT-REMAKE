
undefined4 __thiscall FUN__text1__0080ec70(int param_1,int param_2,int param_3)

{
  uint uVar1;
  uint uVar2;
  undefined4 uVar3;
  
  uVar1 = *(uint *)(*(int *)(param_1 + 0x18) + param_2 * 4);
  uVar2 = *(uint *)(*(int *)(param_1 + 0x18) + param_3 * 4);
  if (uVar1 == uVar2) {
    uVar3 = FUN__text1__0080eb87
                      (*(undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4),
                       *(undefined4 *)(*(int *)(param_1 + 0xc) + param_3 * 4));
  }
  else if (uVar2 < uVar1) {
    uVar3 = 1;
  }
  else {
    uVar3 = 0xffffffff;
  }
  return uVar3;
}


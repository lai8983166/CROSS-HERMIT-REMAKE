
undefined4 __thiscall FUN__text__00548e1c(int *param_1,undefined4 param_2)

{
  undefined4 *puVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  
  if (param_1[1] == param_1[2]) {
    puVar1 = (undefined4 *)FUN__text__00428a40(param_1[2] * 4 + 0x40);
    if (puVar1 == (undefined4 *)0x0) {
      param_1[3] = -0x7ff8fff2;
      return 0x8007000e;
    }
    if ((undefined4 *)*param_1 != (undefined4 *)0x0) {
      puVar4 = (undefined4 *)*param_1;
      puVar5 = puVar1;
      for (uVar2 = param_1[1] & 0x3fffffff; uVar2 != 0; uVar2 = uVar2 - 1) {
        *puVar5 = *puVar4;
        puVar4 = puVar4 + 1;
        puVar5 = puVar5 + 1;
      }
      for (iVar3 = 0; iVar3 != 0; iVar3 = iVar3 + -1) {
        *(undefined1 *)puVar5 = *(undefined1 *)puVar4;
        puVar4 = (undefined4 *)((int)puVar4 + 1);
        puVar5 = (undefined4 *)((int)puVar5 + 1);
      }
      FUN__text__00428ad0(*param_1);
    }
    param_1[2] = param_1[2] + 0x10;
    *param_1 = (int)puVar1;
  }
  *(undefined4 *)(*param_1 + param_1[1] * 4) = param_2;
  param_1[1] = param_1[1] + 1;
  return 0;
}


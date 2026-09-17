
void FUN__text__0054a422(int *param_1)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  int iVar4;
  
  param_1[1] = 0;
  uVar1 = FUN__text__0054d132(param_1);
  puVar2 = (undefined4 *)FUN__text__0054d0ed(param_1,0x50);
  if (puVar2 == (undefined4 *)0x0) {
    FUN__text__0054d135(param_1);
    *(undefined4 *)(*param_1 + 0x14) = 0x35;
    *(undefined4 *)(*param_1 + 0x18) = 0;
    (**(code **)*param_1)(param_1);
  }
  else {
    *puVar2 = FUN__text__00549ac2;
    puVar2[1] = FUN__text__00549bbe;
    puVar2[2] = FUN__text__00549c4c;
    puVar2[3] = FUN__text__00549cde;
    puVar2[4] = FUN__text__00549d7c;
    puVar2[5] = FUN__text__00549ddd;
    puVar2[6] = FUN__text__00549e3e;
    puVar2[7] = FUN__text__0054a0d0;
    puVar2[8] = FUN__text__0054a1ee;
    puVar2[9] = FUN__text__0054a311;
    puVar2[10] = FUN__text__0054a3f2;
    puVar2[0xb] = uVar1;
    puVar3 = puVar2 + 0xf;
    iVar4 = 2;
    do {
      puVar3[-2] = 0;
      *puVar3 = 0;
      puVar3 = puVar3 + -1;
      iVar4 = iVar4 + -1;
    } while (iVar4 != 0);
    puVar2[0x10] = 0;
    puVar2[0x11] = 0;
    puVar2[0x12] = 0x50;
    param_1[1] = (int)puVar2;
  }
  return;
}


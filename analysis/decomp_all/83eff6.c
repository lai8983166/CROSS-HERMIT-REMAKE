
undefined4 FUN__text1__0083eff6(undefined4 *param_1,undefined4 *param_2)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  
  if (((param_2 == (undefined4 *)0x0) || (param_1 == (undefined4 *)0x0)) || (param_2[7] == 0)) {
    uVar2 = 0xfffffffe;
  }
  else {
    puVar1 = (undefined4 *)param_2[7];
    puVar3 = param_1;
    for (iVar4 = 0xe; iVar4 != 0; iVar4 = iVar4 + -1) {
      *puVar3 = *param_2;
      param_2 = param_2 + 1;
      puVar3 = puVar3 + 1;
    }
    puVar3 = (undefined4 *)(*(code *)param_1[8])(param_1[10],1,0x16b8);
    if (puVar3 == (undefined4 *)0x0) {
      uVar2 = 0xfffffffc;
    }
    else {
      param_1[7] = puVar3;
      puVar5 = puVar1;
      puVar6 = puVar3;
      for (iVar4 = 0x5ae; iVar4 != 0; iVar4 = iVar4 + -1) {
        *puVar6 = *puVar5;
        puVar5 = puVar5 + 1;
        puVar6 = puVar6 + 1;
      }
      *puVar3 = param_1;
      uVar2 = (*(code *)param_1[8])(param_1[10],puVar3[9],2);
      puVar3[0xc] = uVar2;
      uVar2 = (*(code *)param_1[8])(param_1[10],puVar3[9],2);
      puVar3[0xe] = uVar2;
      uVar2 = (*(code *)param_1[8])(param_1[10],puVar3[0x11],2);
      puVar3[0xf] = uVar2;
      iVar4 = (*(code *)param_1[8])(param_1[10],puVar3[0x5a5],4);
      puVar3[2] = iVar4;
      if (((puVar3[0xc] == 0) || (puVar3[0xe] == 0)) || ((puVar3[0xf] == 0 || (puVar3[2] == 0)))) {
        FUN__text1__0083eee5(param_1);
        uVar2 = 0xfffffffc;
      }
      else {
        FUN__text1__00848490(puVar3[0xc],puVar1[0xc],puVar3[9] << 1);
        FUN__text1__00848490(puVar3[0xe],puVar1[0xe],puVar3[9] << 1);
        FUN__text1__00848490(puVar3[0xf],puVar1[0xf],puVar3[0x11] << 1);
        FUN__text1__00848490(puVar3[2],puVar1[2],puVar3[3]);
        puVar3[4] = puVar3[2] + (puVar1[4] - puVar1[2]);
        puVar3[0x5a7] = iVar4 + (puVar3[0x5a5] & 0xfffffffe);
        puVar3[0x5a4] = puVar3[2] + puVar3[0x5a5] * 3;
        puVar3[0x2c4] = puVar3 + 0x23;
        puVar3[0x2c7] = puVar3 + 0x260;
        puVar3[0x2ca] = puVar3 + 0x29d;
        uVar2 = 0;
      }
    }
  }
  return uVar2;
}


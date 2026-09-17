
undefined4 FUN__text1__00836e0a(undefined4 param_1,int param_2,uint param_3,int param_4)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  undefined3 uVar6;
  undefined4 *puVar4;
  void *pvVar5;
  
  iVar1 = (int)((param_2 - DAT_008753f4) + (param_2 - DAT_008753f4 >> 0x1f & 0xfffU)) >> 0xc;
  iVar2 = (param_2 - DAT_008753f4) + -1 + param_3;
  iVar2 = (int)(iVar2 + (iVar2 >> 0x1f & 0xfffU)) >> 0xc;
  if (iVar1 == iVar2) {
    puVar4 = operator_new(0x10);
    puVar4[3] = *(undefined4 *)(DAT_008753e8 + iVar1 * 4);
    *(undefined4 **)(DAT_008753e8 + iVar1 * 4) = puVar4;
    puVar4[1] = param_2;
    puVar4[2] = param_3;
    pvVar5 = operator_new(param_3);
    *puVar4 = pvVar5;
    uVar3 = FUN__text1__00848490(*puVar4,param_4,param_3);
    uVar6 = (undefined3)((uint)uVar3 >> 8);
  }
  else {
    iVar2 = (DAT_008753f4 + iVar2 * 0x1000) - param_2;
    FUN__text1__00836e0a(param_1,param_2,iVar2,param_4);
    uVar3 = FUN__text1__00836e0a(param_1,param_2 + iVar2,param_3 - iVar2,param_4 + iVar2);
    uVar6 = (undefined3)((uint)uVar3 >> 8);
  }
  return CONCAT31(uVar6,1);
}


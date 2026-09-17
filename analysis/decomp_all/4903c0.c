
void FUN__text__004903c0(undefined4 param_1,int param_2,undefined4 param_3)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(short *)(param_2 + 0xc) = *(short *)(param_2 + 0xc) + 1;
  sVar1 = *(short *)(param_2 + 0xc);
  if (0xb3 < sVar1) {
    *(undefined2 *)(param_2 + 0xc) = 0;
    FUN__text__00493320(param_3,CONCAT22(sVar1 >> 0xf,*(undefined2 *)(param_2 + 0xe)),0);
  }
  uStack_8 = 0x490425;
  FUN__text__0056ce80();
  return;
}


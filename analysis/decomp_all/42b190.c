
undefined4
FUN__text__0042b190(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [16];
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((((param_1 < param_3) || (param_5 < param_1)) || (param_2 < param_4)) || (param_6 < param_2))
  {
    uVar1 = 0;
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}



void FUN__text__004993d0(undefined4 param_1,short param_2,short param_3,undefined4 param_4,
                        undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00466640(param_1,param_2 * 0x20 + 0x10,param_3 * 0x10 + 8,param_4,param_5,0,0);
  uStack_8 = 0x49942c;
  FUN__text__0056ce80();
  return;
}


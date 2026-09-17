
void FUN__text__004db470(undefined4 param_1,undefined4 param_2,void *param_3)

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
  _memset(param_3,0,0x24);
  FUN__text__004dcf00(param_1,param_2,param_3,1);
  uStack_8 = 0x4db4bb;
  FUN__text__0056ce80();
  return;
}


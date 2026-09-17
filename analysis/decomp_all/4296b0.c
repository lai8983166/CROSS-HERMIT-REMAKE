
void FUN__text__004296b0(undefined4 param_1,void *param_2)

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
  _memset(param_2,0,0x303);
  FUN__text__00570b20(param_1,param_2,(int)param_2 + 3,(int)param_2 + 0x103,(int)param_2 + 0x203);
  uStack_8 = 0x429716;
  FUN__text__0056ce80();
  return;
}


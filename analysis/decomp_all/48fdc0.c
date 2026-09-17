
void FUN__text__0048fdc0(undefined4 param_1,undefined1 *param_2,undefined4 param_3,int param_4)

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
  *param_2 = 0x35;
  *(undefined2 *)(param_2 + 0xe) = *(undefined2 *)(param_4 + 0xe);
  *(undefined4 *)(param_2 + 8) = *(undefined4 *)(param_4 + 8);
  *(undefined2 *)(param_2 + 4) = *(undefined2 *)(param_4 + 4);
  FUN__text__0046beb0(param_3,(int)DAT_00615e3a,0,0,4,0);
  FUN__text__00495130(param_3,0xe);
  uStack_8 = 0x48fe3d;
  FUN__text__0056ce80();
  return;
}


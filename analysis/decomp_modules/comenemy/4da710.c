
void FUN__text__004da710(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(byte *)(*(int *)(param_2 + 600) + 0xa4) < 4) {
    iVar2 = FUN__text__00424f80("4 <= wk->data->player",
                                "e:\\crosshermit\\game\\src\\common\\comenemy.cpp",DAT_006a88d0 + 2,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  puVar3 = (undefined4 *)(param_1 + 0x14);
  puVar4 = (undefined4 *)(param_2 + 0x2ac);
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  *(undefined4 *)(param_2 + 0x2d4) = 0;
  *(undefined4 *)(param_2 + 0x2d8) = 0;
  *(undefined4 *)(param_2 + 0x2dc) = 0;
  *(undefined4 *)(param_2 + 0x2e0) = 0;
  *(undefined1 *)(param_2 + 0x2e8) = 0;
  *(undefined1 *)(param_2 + 0x2e9) = 0;
  *(undefined2 *)(*(int *)(param_2 + 600) + 0xa8) = *(undefined2 *)(param_1 + 0x10);
  uStack_8 = 0x4da7e4;
  FUN__text__0056ce80();
  return;
}


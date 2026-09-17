
void FUN__text__004dfa70(byte *param_1,undefined4 param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((*param_1 != 0) && (*(int *)(param_1 + 8) != 0)) {
    if ((0x45 < *param_1) &&
       (iVar2 = FUN__text__00424f80("cond->type<=(69)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738ca4 + 0x4c,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (*(int *)(&DAT_00738af8 + (uint)*param_1 * 4) != 0) {
      (**(code **)(&DAT_00738af8 + (uint)*param_1 * 4))(param_1,param_2,param_3);
      FUN__text__0056ce80();
    }
  }
  uStack_8 = 0x4dfb16;
  FUN__text__0056ce80();
  return;
}



void FUN__text__00449650(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 < 0) || (1 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=type) && (type<=1)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_0060674c + 3,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__0044bf40(param_1);
  FUN__text__00428220(CONCAT22(extraout_var,(undefined2)local_c),7);
  local_8 = 0x4496c8;
  FUN__text__0056ce80();
  return;
}


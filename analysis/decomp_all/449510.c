
void FUN__text__00449510(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 != 0) && (param_1 != 1)) {
    iVar2 = FUN__text__00424f80("(type==0) || (type==1)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606748 + 3,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__00428310();
  local_10 = FUN__text__0044c000(param_1,local_c);
  local_8 = 0x449595;
  FUN__text__0056ce80();
  return;
}



void __thiscall FUN__text__0044a640(int param_1,int param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 != 0) && (param_2 != 1)) {
    iVar2 = FUN__text__00424f80("(type==0) || (type==1)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",DAT_00606760 + 5,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = local_8 + 0x8a60 + param_2 * 8;
  local_10 = FUN__text__0044bed0(param_2);
  local_14 = FUN__text__0044c150(local_10,param_3);
  FUN__text__004283e0(local_14);
  local_8 = 0x44a6da;
  FUN__text__0056ce80();
  return;
}


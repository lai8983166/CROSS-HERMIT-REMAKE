
void __thiscall FUN__text__0044e650(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 0xb4 + param_2 * 4);
  if ((param_3 < 0) || (*(int *)(local_c + 0x14) <= param_3)) {
    local_8 = param_1;
    iVar2 = FUN__text__00424f80("(0<=no)&&(no<rwk->cnt)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\PathFind.cpp",DAT_0060693c + 4
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = *(undefined4 *)(local_c + 0x18 + param_3 * 4);
  local_8 = 0x44e6cf;
  FUN__text__0056ce80();
  return;
}


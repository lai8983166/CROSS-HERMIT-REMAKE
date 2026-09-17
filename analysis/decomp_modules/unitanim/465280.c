
void __thiscall
FUN__text__00465280(int param_1,int param_2,int param_3,undefined2 param_4,undefined2 param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(short *)(param_1 + 0x48) != -1) {
    *(undefined2 *)(param_2 + 0xc) = (undefined2)param_3;
    local_8 = param_1;
    if ((param_3 < 1000) &&
       (iVar2 = FUN__text__00424f80("ano>=1000","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitAnim.cpp",
                                    DAT_00610530 + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = param_3 / 1000 + -1;
    local_10 = param_3 % 1000;
    if (((local_c < 0) || (3 < local_c)) &&
       (iVar2 = FUN__text__00424f80("(0<=off)&&(off<= 3)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitAnim.cpp",
                                    DAT_00610530 + 0xb,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (((local_10 < 0) || (199 < local_10)) &&
       (iVar2 = FUN__text__00424f80("(0<=no )&&(no <=199)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitAnim.cpp",
                                    DAT_00610530 + 0xc,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_14 = &DAT_0060f890 + local_10 * 4 + local_c * 800;
    *(undefined1 *)(param_2 + 2) = 1;
    FUN__text__00409ff0(param_2,local_14[1],local_14[2],0);
    *(undefined2 *)(param_2 + 0x12) = param_4;
    *(undefined2 *)(param_2 + 0x14) = param_5;
  }
  local_8 = 0x4653c8;
  FUN__text__0056ce80();
  return;
}


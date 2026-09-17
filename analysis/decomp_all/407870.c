
void __thiscall FUN__text__00407870(int param_1,undefined4 param_2,undefined4 param_3)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_48 [16];
  int local_8;
  
  puVar4 = local_48;
  for (iVar3 = 0x11; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x4c) == 0) {
    FUN__text__0042b2d0(&DAT_00592728);
    iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\D3DxSp.cpp",
                                DAT_005ff0b4 + 4,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *(ushort *)(param_1 + 0x58) = *(ushort *)(param_1 + 0x58) | 0x80;
    uVar2 = FUN__text__0041f5a0(param_2,param_3);
    *(undefined4 *)(local_8 + 0x48) = uVar2;
    if ((*(int *)(local_8 + 0x48) == 0) &&
       (iVar3 = FUN__text__00424f80("TexTbl!=0",
                                    "E:\\CrossHermit\\GAME\\src\\system\\directx\\D3DxSp.cpp",
                                    DAT_005ff0b4 + 10,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (*(int *)(local_8 + 0x48) != 0) {
      *(undefined2 *)(local_8 + 0x38) = *(undefined2 *)(*(int *)(local_8 + 0x48) + 0x38);
      *(undefined2 *)(local_8 + 0x3a) = *(undefined2 *)(*(int *)(local_8 + 0x48) + 0x3a);
      *(undefined2 *)(local_8 + 0x3c) = *(undefined2 *)(*(int *)(local_8 + 0x48) + 0x3c);
      *(undefined2 *)(local_8 + 0x3e) = *(undefined2 *)(*(int *)(local_8 + 0x48) + 0x3e);
      *(undefined4 *)(local_8 + 0x34) = *(undefined4 *)(*(int *)(local_8 + 0x48) + 0x34);
      uVar2 = FUN__text__004142b0();
      *(undefined4 *)(local_8 + 0x28) = uVar2;
    }
  }
  local_8 = 0x4079ba;
  FUN__text__0056ce80();
  return;
}


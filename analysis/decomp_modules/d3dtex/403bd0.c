
void __thiscall FUN__text__00403bd0(int param_1,int *param_2,int param_3)

{
  code *pcVar1;
  undefined2 extraout_var;
  int iVar2;
  undefined2 extraout_var_00;
  undefined4 *puVar3;
  undefined4 local_78 [16];
  undefined1 local_38 [16];
  int local_28;
  undefined2 local_20;
  undefined2 local_1c;
  short local_18;
  short local_14;
  int local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_78;
  for (iVar2 = 0x1d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((*(short *)(param_1 + 0x38) != 0) && (*(short *)(param_1 + 0x3a) != 0)) &&
     (*(int *)(param_1 + 0x34) != 0)) {
    local_c = (uint)(param_3 != 0);
    local_8 = param_1;
    FUN__text__00403730();
    local_14 = FUN__text__00403b70(CONCAT22(extraout_var,*(undefined2 *)(local_8 + 0x38)));
    local_18 = FUN__text__00403b70(CONCAT22(extraout_var_00,*(undefined2 *)(local_8 + 0x3a)));
    (**(code **)(*param_2 + 0x50))
              (param_2,(int)local_14,(int)local_18,1,local_c,*(undefined4 *)(local_8 + 0x34),1,
               local_8 + 0x2c);
    local_10 = FUN__text__0056ce80();
    if (-1 < local_10) {
      (**(code **)(**(int **)(local_8 + 0x2c) + 0x38))(*(undefined4 *)(local_8 + 0x2c),0,local_38);
      local_10 = FUN__text__0056ce80();
      if ((local_10 < 0) &&
         (iVar2 = FUN__text__00424f80("((HRESULT)(ret) >= 0)",
                                      "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                      DAT_005ff088 + 0x1c,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *(undefined2 *)(local_8 + 0x3c) = local_20;
      *(undefined2 *)(local_8 + 0x3e) = local_1c;
      PTR_DAT_00765720 = PTR_DAT_00765720 + local_28;
      *(ushort *)(local_8 + 0x44) = *(ushort *)(local_8 + 0x44) | 2;
      *(int **)(local_8 + 0x28) = param_2;
    }
  }
  local_8 = 0x403d3e;
  FUN__text__0056ce80();
  return;
}


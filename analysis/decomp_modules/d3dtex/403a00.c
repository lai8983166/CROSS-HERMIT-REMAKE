
void __fastcall FUN_00403a00(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_6c [16];
  int local_2c;
  undefined1 local_28 [32];
  int local_8;
  
  puVar3 = local_6c;
  for (iVar2 = 0x1a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 0x2c) + 0x38))(*(undefined4 *)(param_1 + 0x2c),0,local_28);
    local_2c = __chkesp();
    if ((local_2c < 0) &&
       (iVar2 = FUN_00424f80("!\"SysD3DTex::GetTextureSize()\"",
                             "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                             DAT_005ff084 + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x403a95;
  __chkesp();
  return;
}


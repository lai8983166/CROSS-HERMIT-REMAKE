
void __fastcall FUN__text__004037f0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  int local_30;
  int local_2c [8];
  int local_c;
  int local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 0x2c) + 0x38))(*(undefined4 *)(param_1 + 0x2c),0,local_2c);
    local_c = FUN__text__0056ce80();
    if (-1 < local_c) {
      local_30 = local_2c[0] + -0x14;
      switch(local_2c[0]) {
      case 0x14:
      case 0x15:
      case 0x16:
      case 0x1f:
      case 0x3e:
      case 0x3f:
      case 0x40:
      case 0x41:
      case 0x43:
        break;
      case 0x17:
      case 0x18:
      case 0x19:
      case 0x1a:
      case 0x1b:
      case 0x1d:
      case 0x1e:
      case 0x22:
      case 0x28:
      case 0x33:
      case 0x3c:
      case 0x3d:
        break;
      case 0x1c:
      case 0x29:
      case 0x32:
      case 0x34:
        break;
      default:
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff080 + 0x26,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
    }
  }
  local_8 = 0x4038c9;
  FUN__text__0056ce80();
  return;
}


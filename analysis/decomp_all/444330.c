
void __thiscall FUN__text__00444330(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(int *)(param_1 + 0x30) = param_2;
  local_8 = param_1;
  FUN__text__00444620();
  FUN__text__0044d040();
  FUN__text__00444590();
  FUN__text__004415e0(DAT_007a49fc);
  FUN__text__00415420();
  FUN__text__00422360(0);
  if (param_2 != 0) {
    *(undefined4 *)(local_8 + 0x1a50) = 10;
  }
LAB__text__004443ad:
  local_10 = *(undefined4 *)(local_8 + 0x1a50);
  switch(local_10) {
  case 0:
    FUN__text__00444820();
    goto LAB__text__004443ad;
  case 1:
    FUN__text__00444960();
    goto LAB__text__004443ad;
  case 2:
    FUN__text__00444960();
  case 3:
    FUN__text__00439e30(1);
    FUN__text__00422360(10);
    local_c = FUN__text__00417cc0();
    if ((local_c != 0) &&
       (iVar2 = FUN__text__00424f80("ret == 0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                    DAT_00606710 + 0x72,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 4:
    FUN__text__00439e30(0x10);
    break;
  case 5:
    FUN__text__00444a90();
    goto LAB__text__004443ad;
  case 6:
    FUN__text__00444e60();
    goto LAB__text__004443ad;
  case 7:
    FUN__text__00445150(0);
    goto LAB__text__004443ad;
  case 8:
    FUN__text__00446780(0);
    goto LAB__text__004443ad;
  case 9:
    FUN__text__00444960();
  case 10:
    local_14 = FUN__text__004478e0();
    if (local_14 == 0) {
      *(undefined4 *)(local_8 + 0x1a50) = 6;
    }
    else if (local_14 == 1) {
      *(undefined4 *)(local_8 + 0x1a50) = 0xb;
    }
    else if (local_14 == 2) {
      *(undefined4 *)(local_8 + 0x1a50) = 3;
    }
    goto LAB__text__004443ad;
  case 0xb:
    FUN__text__00448650();
    goto LAB__text__004443ad;
  default:
    goto code_r0x004444c5;
  }
  FUN__text__00422360(10);
  local_8 = 0x444553;
  FUN__text__0056ce80();
  return;
code_r0x004444c5:
  iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                              DAT_00606710 + 0x6a,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  goto LAB__text__004443ad;
}



void FUN__text__0046c350(int param_1,int param_2)

{
  ushort uVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((param_2 == 0) && (*(char *)(*(int *)(param_1 + 600) + 0x9d) != '\0')) {
    uVar1 = *(ushort *)
             (*(int *)(param_1 + 600) + 0x84 + (uint)*(byte *)(*(int *)(param_1 + 600) + 0x9e) * 2);
    local_c = CONCAT22(local_c._2_2_,uVar1);
    if (uVar1 != 0) {
      if ((uVar1 & 0x8000) != 0) goto LAB__text__0046c465;
      local_c = CONCAT22(local_c._2_2_,uVar1) & 0xffff7fff;
      if ((0x3ff < (uVar1 & 0x7fff)) &&
         (iVar3 = FUN__text__00424f80("(0<=no) && (no<1024)",
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                      DAT_00618c0c + 0x12,0), iVar3 != 0)) {
        pcVar2 = (code *)swi(3);
        (*pcVar2)();
        return;
      }
      if ((&DAT_006c2dcd)[(local_c & 0xffff) * 0x48] != '\x03') goto LAB__text__0046c465;
    }
  }
  local_c = CONCAT22(local_c._2_2_,
                     *(undefined2 *)
                      (&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40));
LAB__text__0046c465:
  local_8 = 0x46c472;
  FUN__text__0056ce80();
  return;
}


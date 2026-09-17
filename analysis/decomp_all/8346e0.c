
/* WARNING: Instruction at (ram,0x00834708) overlaps instruction at (ram,0x00834707)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x00834abd) */
/* WARNING: Removing unreachable block (ram,0x0083492f) */
/* WARNING: Removing unreachable block (ram,0x00834895) */
/* WARNING: Removing unreachable block (ram,0x0083474c) */
/* WARNING: Removing unreachable block (ram,0x008346f0) */
/* WARNING: Removing unreachable block (ram,0x0083470d) */
/* WARNING: Removing unreachable block (ram,0x00834690) */
/* WARNING: Removing unreachable block (ram,0x008346b0) */
/* WARNING: Removing unreachable block (ram,0x008346c6) */
/* WARNING: Removing unreachable block (ram,0x00834700) */
/* WARNING: Removing unreachable block (ram,0x00834839) */
/* WARNING: Removing unreachable block (ram,0x008348f2) */
/* WARNING: Removing unreachable block (ram,0x008348d5) */
/* WARNING: Removing unreachable block (ram,0x00834a44) */
/* WARNING: Removing unreachable block (ram,0x008348a3) */
/* WARNING: Removing unreachable block (ram,0x00834acb) */
/* WARNING: Removing unreachable block (ram,0x008349c5) */
/* WARNING: Removing unreachable block (ram,0x00834875) */
/* WARNING: Removing unreachable block (ram,0x008349cb) */
/* WARNING: Removing unreachable block (ram,0x00834b03) */
/* WARNING: Removing unreachable block (ram,0x00834b05) */
/* WARNING: Removing unreachable block (ram,0x008348e5) */
/* WARNING: Removing unreachable block (ram,0x0083475a) */
/* WARNING: Removing unreachable block (ram,0x008349d5) */
/* WARNING: Removing unreachable block (ram,0x00834965) */
/* WARNING: Removing unreachable block (ram,0x008349e2) */
/* WARNING: Removing unreachable block (ram,0x008349e1) */
/* WARNING: Removing unreachable block (ram,0x008349e6) */
/* WARNING: Heritage AFTER dead removal. Example location: s0xffffffd8 : 0x008348b7 */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

undefined4 FUN__text1__008346e0(uint *param_1)

{
  uint uVar1;
  char cVar2;
  void *pvVar3;
  int iVar4;
  LPVOID pvVar5;
  undefined4 uVar6;
  BOOL BVar7;
  int unaff_EBX;
  undefined1 *puVar8;
  undefined1 *unaff_ESI;
  undefined1 *puStackY_ec;
  int iStackY_e4;
  undefined1 *in_stack_ffffff2c;
  int in_stack_ffffff34;
  undefined1 *puStack_bc;
  undefined1 *puStack_b8;
  
  uVar1 = *param_1;
  *(byte *)(unaff_EBX + -0x7b276f8) = *(byte *)(unaff_EBX + -0x7b276f8) | (byte)uVar1;
  pvVar3 = operator_new(uVar1);
  do {
    iVar4 = FUN__text1__00834599();
    if (iVar4 == 0) {
      return 0;
    }
  } while (uVar1 != 0);
  puStack_b8 = &stack0xffffff5c;
  puStack_bc = &stack0xfffffffc;
  pvVar5 = VirtualAlloc(*(LPVOID *)((int)pvVar3 + *(int *)((int)pvVar3 + 0x3c) + 0x34),
                        *(SIZE_T *)((int)pvVar3 + *(int *)((int)pvVar3 + 0x3c) + 0x50),0x1000,4);
  puVar8 = &stack0xfffffffc;
  if (((pvVar5 == (LPVOID)0x0) &&
      (unaff_EBX = in_stack_ffffff34, puVar8 = in_stack_ffffff2c, puStack_bc = unaff_ESI,
      puStack_b8 = &stack0xfffffffc, 5 < *(uint *)(*(int *)(in_stack_ffffff2c + -0x28) + 0x5c))) &&
     (puStack_b8 = &stack0xfffffffc,
     *(int *)(CONCAT22((short)((uint)*(undefined4 *)(in_stack_ffffff2c + -0x28) >> 0x10),
                       *(undefined2 *)(in_stack_ffffff2c + -0x28)) + 0x88) != 0)) {
    puStack_b8 = &stack0xfffffffc;
    pvVar5 = VirtualAlloc((LPVOID)0x0,*(SIZE_T *)(in_stack_ffffff2c + -0x10),0x1000,4);
    *(LPVOID *)(in_stack_ffffff2c + -0x20) = pvVar5;
  }
  if (*(int *)(puVar8 + -0x20) == 0) {
    DAT_008750d8 = 2;
    uVar6 = 0;
  }
  else {
    FUN__text1__00848490();
    *(undefined4 *)(puVar8 + -0xc) = *(undefined4 *)(puVar8 + -0x18);
    *(uint *)(puVar8 + -0x14) =
         *(int *)(puVar8 + -0xc) + (uint)*(ushort *)(*(int *)(puVar8 + -0x2c) + 2) * 0x28;
    while (iVar4 = iStackY_e4, *(uint *)(puVar8 + -0xc) < *(uint *)(puVar8 + -0x14)) {
      iStackY_e4 = 0x834a04;
      FUN__text1__00848490
                (*(int *)(puStackY_ec + -0x20) + *(int *)(*(int *)(puStackY_ec + -0xc) + 0xc),
                 *(int *)(puStackY_ec + -0x30) + *(int *)(*(int *)(puStackY_ec + -0xc) + 0x14),
                 *(undefined4 *)(*(int *)(puStackY_ec + -0xc) + 0x10),puVar8,&puStack_bc,unaff_EBX);
      *(int *)(puStackY_ec + -0xc) = *(int *)(puStackY_ec + -0xc) + 0x28;
      unaff_EBX = iVar4;
      puVar8 = puStackY_ec;
    }
    if (*(int *)(puVar8 + -0x20) != *(int *)(puVar8 + -0x24)) {
      *(int *)(puVar8 + -0x40) =
           *(int *)(puVar8 + -0x20) + *(int *)(*(int *)(puVar8 + -0x28) + 0x88);
      *(undefined4 *)(puVar8 + -0x3c) = *(undefined4 *)(*(int *)(puVar8 + -0x28) + 0x8c);
      cVar2 = FUN__text1__00834c73(*(undefined4 *)(puVar8 + -0x20));
      if (cVar2 == '\0') {
        return 0;
      }
    }
    cVar2 = FUN__text1__00834df7();
    if (cVar2 == '\0') {
      uVar6 = 0;
    }
    else {
      *(undefined4 *)(puVar8 + -0xc) = *(undefined4 *)(puVar8 + -0x18);
      while (*(uint *)(puVar8 + -0xc) < *(uint *)(puVar8 + -0x14)) {
        *(undefined4 *)(puVar8 + -0x50) = *(undefined4 *)(*(int *)(puVar8 + -0xc) + 0x24);
        puVar8[-0x58] = 0;
        puVar8[-0x54] = 0;
        puVar8[-0x4c] = 0;
        if ((*(uint *)(puVar8 + -0x50) & 0x20000020) != 0) {
          puVar8[-0x4c] = 1;
        }
        if ((*(uint *)(puVar8 + -0x50) & 0x40000000) != 0) {
          puVar8[-0x58] = 1;
        }
        if ((*(uint *)(puVar8 + -0x50) & 0x80000000) != 0) {
          puVar8[-0x54] = 1;
        }
        *(undefined4 *)(puVar8 + -0x44) = 1;
        if ((*(uint *)(puVar8 + -0x4c) & 0xff) == 0) {
          if ((*(uint *)(puVar8 + -0x58) & 0xff) != 0) {
            if ((*(uint *)(puVar8 + -0x54) & 0xff) == 0) {
              *(undefined4 *)(puVar8 + -0x44) = 2;
            }
            else {
              *(undefined4 *)(puVar8 + -0x44) = 4;
            }
          }
        }
        else if ((*(uint *)(puVar8 + -0x54) & 0xff) == 0) {
          if ((*(uint *)(puVar8 + -0x58) & 0xff) == 0) {
            *(undefined4 *)(puVar8 + -0x44) = 0x10;
          }
          else {
            *(undefined4 *)(puVar8 + -0x44) = 0x20;
          }
        }
        else {
          *(undefined4 *)(puVar8 + -0x44) = 0x40;
        }
        *(int *)(puVar8 + -0x60) =
             *(int *)(puVar8 + -0x20) + *(int *)(*(int *)(puVar8 + -0xc) + 0xc);
        *(undefined4 *)(puVar8 + -0x48) = *(undefined4 *)(*(int *)(puVar8 + -0xc) + 8);
        BVar7 = VirtualProtect(*(LPVOID *)(puVar8 + -0x60),*(SIZE_T *)(puVar8 + -0x48),
                               *(DWORD *)(puVar8 + -0x44),(PDWORD)(puVar8 + -0x5c));
        if (BVar7 == 0) {
          DAT_008750d8 = 4;
          return 0;
        }
        *(int *)(puVar8 + -0xc) = *(int *)(puVar8 + -0xc) + 0x28;
      }
      DAT_008750d0 = *(int *)(puVar8 + -0x20) + *(int *)(*(int *)(puVar8 + -0x28) + 0x10);
      *(undefined4 *)(puVar8 + -0x68) = *(undefined4 *)(puVar8 + -0x30);
      FUN__text1__00848476();
      DAT_008750cc = *(undefined4 *)(puVar8 + -0x20);
      uVar6 = *(undefined4 *)(puVar8 + 8);
    }
  }
  return uVar6;
}

